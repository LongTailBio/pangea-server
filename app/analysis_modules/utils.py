"""Utilities for the Conductor module."""

from uuid import UUID
from pprint import pformat
from time import sleep

from flask import current_app
from mongoengine.errors import ValidationError

from analysis_packages.base.exceptions import UnsupportedAnalysisMode

from app.analysis_modules import all_analysis_modules, MODULES_BY_NAME
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.extensions import celery, celery_logger, persist_result_lock
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup
from app.utils import lock_function

from .tasks import clean_error

BLOCK_TIME = 100


def fetch_samples(sample_group_id):
    """Get all samples belonging to the specified Sample Group."""
    sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
    samples = [sample.fetch_safe() for sample in sample_group.samples]
    return samples


def filter_samples(samples, module):
    """Filter list of samples to only those supporting the given module."""
    dependencies = {upstream.name() for upstream in module.required_modules()}

    def test_sample(sample):
        """Return true if a sample has all upstreams required by the module."""
        analysis_result_uuid = sample.analysis_result_uuid
        analysis_result = AnalysisResultMeta.objects.get(uuid=analysis_result_uuid)
        tools_present = analysis_result.result_types()
        is_valid = dependencies <= tools_present
        current_app.logger.debug(f'Testing sample: {sample.name}')
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
    task_signatures = [sig.on_error(clean_error.s()) for sig in task_signatures if sig is not None]
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


def block_if_analysis_result_exists(module, analysis_result):
    """Block while A.R. exists but is not complete, return False iff A.R. should be rerun."""
    if (module.name() in analysis_result.result_types() and
            getattr(analysis_result, module.name()).fetch() != 'E'):
        # Block if the result exists and isn't in error then return early
        while getattr(analysis_result, module.name()).fetch() not in ['S', 'E']:
            sleep(BLOCK_TIME)
        return True
    return False


def task_body_sample(sample_uuid, module):
    """Wrap analysis work with status update operations."""
    uuid = UUID(sample_uuid)
    sample = Sample.objects.get(uuid=uuid)
    analysis_result = sample.analysis_result.fetch()
    if block_if_analysis_result_exists(module, analysis_result):
        return
    analysis_result.set_module_status(module.name(), 'W')
    tool_names = [tool.name() for tool in module.required_tool_results()]
    sample = sample.fetch_safe(tool_names)
    data = module.single_sample_processor()(sample)
    persist_result_helper(analysis_result, module, data)


@celery.task()
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

    def build_sample_sig(sample_uuid, module_name):
        """Return a signature for a sample task."""
        return run_sample.s(sample_uuid, module_name).on_error(clean_error.s())

    if not module_names:
        module_names = list(MODULES_BY_NAME.keys())

    task_signatures = build_module_digraph(
        sample_uuid,
        module_names,
        build_sample_sig,
    )
    return task_signatures


def task_body_sample_group(sample_group_uuid, module):
    """Wrap analysis work for SampleGroup."""
    sample_group = SampleGroup.query.filter_by(id=sample_group_uuid).one()
    if block_if_analysis_result_exists(module, sample_group.analysis_result):
        return
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


@celery.task()
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

    def build_sample_group_sig(sample_group_uuid, module_name):
        """Return a signature for a sample group task."""
        return run_sample_group.s(sample_group_uuid, module_name).on_error(clean_error.s())

    if not module_names:
        module_names = list(MODULES_BY_NAME.keys())

    task_signatures = build_module_digraph(
        sample_group_uuid,
        module_names,
        build_sample_group_sig,
    )
    return task_signatures


def build_module_digraph(uuid, module_names, signature_builder):
    """Build a tree of tasks based on module dependencies."""

    def recurse_depends(source_module, depend_graph):
        """Recursively add dependency edges to the depend graph."""
        for depends_module in source_module.required_modules():
            depend_graph.add_edge(source_module.name(), depends_module.name())
            recurse_depends(depends_module, depend_graph)

    depend_graph = nx.DiGraph()
    for module_name in module_names:
        source_module = MODULES_BY_NAME[module_name]
        recurse_depends(source_module, depend_graph)
    signature_tbl = {}

    def recurse_chords(source_module_name):
        """Build a tree of tasks."""
        try:
            source_signature = signature_tbl[source_module_name]
        except KeyError:
            source_signature = signature_builder(uuid, source_module_name)
            signature_tbl[source_module_name] = source_signature
        depends_on_chord = [
            recurse_chords(upstream_name)
            for upstream_name in nx.descendants(depends_graph, source_module_name)
        ]
        if not depends_on_chord:
            return source_signature
        return chord(depends_on_chord) | source_signature

    task_signatures = [
        recurse_chords(module_name)
        for module_name in depend_graph.nodes()
        if depend_graph.in_degree(module_name) == 0
    ]
    return task_signatures







