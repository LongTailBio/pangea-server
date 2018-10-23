"""Utilities for the Conductor module."""

from uuid import UUID
from pprint import pformat

from flask import current_app
from mongoengine.errors import ValidationError

from analysis_packages.base.exceptions import UnsupportedAnalysisMode

from app.analysis_modules import all_analysis_modules, MODULES_BY_NAME
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.extensions import celery, celery_logger, persist_result_lock
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results import all_tool_results
from app.utils import lock_function

from .tasks import PluginTask


def apply_errback(signatures):
    """Add error callback to list of signatures."""
    return [sig for sig in signatures if sig is not None]


def fetch_samples(sample_group_id):
    """Get all samples belonging to the specified Sample Group."""
    sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
    samples = [sample.fetch_safe() for sample in sample_group.samples]
    return samples


def filter_samples(samples, module):
    """Filter list of samples to only those supporting the given module."""
    dependencies = {tool.name() for tool in module.required_tool_results()}

    def test_sample(sample):
        """Test a single sample to see if it has all tools required by the display module."""
        all_fields = [mod.name() for mod in all_tool_results]
        tools_present = {field for field in all_fields
                         if getattr(sample, field, None) is not None}
        is_valid = dependencies <= tools_present
        sample_name = sample.name
        current_app.logger.debug(f'Testing sample: {sample_name}')
        current_app.logger.debug(f'Tools present: {tools_present}')
        current_app.logger.debug(f'Is valid: {is_valid}')
        return is_valid

    result = [sample for sample in samples if test_sample(sample)]
    current_app.logger.debug(f'result: {result}')
    return result


def sample_group_middleware(sample_group_id, *module_names):
    """
    Gather task signatures for sample group.

    *module_names are analysis module names. If not provided, all analysis modules will be run.
    """
    if not module_names:
        module_names = list(MODULES_BY_NAME.keys())
    modules = all_analysis_modules
    if module_names:
        # Raises KeyError for unrecognized module names
        modules = [MODULES_BY_NAME[module_name] for module_name in module_names]

    task_signatures = [module.group_signature(sample_group_id) for module in modules]
    task_signatures = apply_errback(task_signatures)
    return task_signatures


@lock_function(persist_result_lock)
def persist_result_helper(result_base, module, data):
    """Persist results to an Analysis Result model."""
    analysis_name = module.name()
    analysis_result = module.result_model()(**data)
    result_wrapper = getattr(result_base, analysis_name).fetch()
    try:
        result_wrapper.data = analysis_result
        result_wrapper.status = 'S'
        result_wrapper.save()
        result_base.save()
    except ValidationError:
        contents = pformat(data)
        celery_logger.exception('Could not save result with contents:\n%s', contents)

        result_wrapper.data = None
        result_wrapper.status = 'E'
        result_wrapper.save()
        result_base.save()


def task_body_sample(sample_uuid, module):
    """Wrap analysis work with status update operations."""
    uuid = UUID(sample_uuid)
    sample = Sample.objects.get(uuid=uuid)
    analysis_result = sample.analysis_result.fetch()
    analysis_result.set_module_status(module.name(), 'W')
    tool_names = [tool.name() for tool in module.required_tool_results()]
    sample = sample.fetch_safe(tool_names)
    data = module.single_sample_processor()(sample)
    persist_result_helper(analysis_result, module, data)


@celery.task(base=PluginTask)
def run_sample(sample_uuid, module_name):
    """Wrap analysis work for single Sample."""
    try:
        module = MODULES_BY_NAME[module_name]
    except KeyError:
        # This should raise a AnalysisNotFound exception to be handled by clean_error
        return

    try:
        _ = module.single_sample_processor()
        task_body_sample(sample_uuid, module)
    except UnsupportedAnalysisMode:
        pass


def conduct_sample(sample_uuid, module_names):
    """Orchestrate tasks to be run for a Sample middleware call."""
    if not module_names:
        module_names = list(MODULES_BY_NAME.keys())

    task_signatures = [run_sample.s(sample_uuid, module_name)
                       for module_name in module_names]
    task_signatures = apply_errback(task_signatures)
    return task_signatures


def task_body_sample_group(sample_group_uuid, module):
    """Wrap analysis work for SampleGroup."""
    sample_group = SampleGroup.query.filter_by(id=sample_group_uuid).one()
    sample_group.analysis_result.set_module_status(module.name(), 'W')
    samples = filter_samples(sample_group.samples, module)
    tool_names = [tool.name() for tool in module.required_tool_results()]
    samples = [sample.fetch_safe(tool_names) for sample in samples]
    data = module.samples_processor()(*samples)
    analysis_result_uuid = sample_group.analysis_result_uuid
    analysis_result = AnalysisResultMeta.objects.get(uuid=analysis_result_uuid)
    persist_result_helper(analysis_result, module, data)


def task_body_group_tool_result(sample_group_uuid, module):
    """Wrap analysis work for a SampleGroup's GroupToolResult."""
    sample_group = SampleGroup.query.filter_by(id=sample_group_uuid).one()
    sample_group.analysis_result.set_module_status(module.name(), 'W')
    group_tool_cls = module.required_tool_results()[0].result_model()
    group_tool = group_tool_cls.objects.get(sample_group_uuid=sample_group.id)
    data = module.group_tool_processor()(group_tool)
    analysis_result_uuid = sample_group.analysis_result_uuid
    analysis_result = AnalysisResultMeta.objects.get(uuid=analysis_result_uuid)
    persist_result_helper(analysis_result, module, data)


@celery.task(base=PluginTask)
def run_sample_group(sample_group_uuid, module_name):
    """Run middleware for a sample group."""
    try:
        module = MODULES_BY_NAME[module_name]
    except KeyError:
        # This should raise a AnalysisNotFound exception to be handled by clean_error
        return

    try:
        _ = module.group_tool_processor()
        task_body_group_tool_result(sample_group_uuid, module)
    except UnsupportedAnalysisMode:
        pass

    try:
        _ = module.samples_processor()
        task_body_sample_group(sample_group_uuid, module)
    except UnsupportedAnalysisMode:
        pass


def conduct_sample_group(sample_group_uuid, module_names):
    """Orchestrate tasks to be run for a SampleGroup middleware call."""
    if not module_names:
        module_names = list(MODULES_BY_NAME.keys())

    task_signatures = [run_sample_group.s(sample_group_uuid, module_name)
                       for module_name in module_names]
    task_signatures = apply_errback(task_signatures)
    return task_signatures
