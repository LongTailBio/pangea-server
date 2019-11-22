"""Tasks for the Conductor module."""

from uuid import UUID

from pangea_modules.base.exceptions import UnsupportedAnalysisMode

from app.extensions import celery
from app.analysis_modules import MODULES_BY_NAME
from app.db_models import SampleGroup, Sample


@celery.task(bind=True)
def clean_error(self):
    """Handle expected error types cleanly.

    To be used like: module_task.s(sample_group_id).on_error(clean_error.s()).delay()
    """
    pass


def generic_task_body(result_parent, module, processor, data_in):
    """Wrap analysis work for SampleGroup."""
    result = result_parent.analysis_result(module.name())
    if result.status in ['WORKING', 'SUCCESS']:
        return
    result.set_status('WORKING')
    try:
        data = processor(data_in)
        for key, val in data.items():
            result_field = result.field(key)
            result_field.set_data(val)
        result.set_status('SUCCESS')
    except Exception:
        result.set_status('ERROR')


@celery.task()
def run_sample(sample_uuid, module_name, dependency_names):
    """Wrap analysis work for single Sample."""
    try:
        module = MODULES_BY_NAME[module_name]
    except KeyError:
        # This should raise a AnalysisNotFound exception to be handled by clean_error
        return

    try:
        processor = module.single_sample_processor()
        sample = Sample.query.filter_by(uuid=UUID(sample_uuid)).first()
        for depends_name in dependency_names:
            if sample.analysis_result(depends_name).status != 'SUCCESS':
                return
        generic_task_body_sample(sample, module, processor, sample)

    except UnsupportedAnalysisMode:
        pass


@celery.task()
def run_sample_group(sample_group_uuid, module_name, dependency_names):
    """Run middleware for a sample group."""
    try:
        module = MODULES_BY_NAME[module_name]
    except KeyError:
        # This should raise a AnalysisNotFound exception to be handled by clean_error
        return

    sample_group = SampleGroup.query.filter_by(uuid=UUID(sample_group_uuid)).first()
    try:
        processor = module.group_tool_processor()
        for depends_name in dependency_names:
            if sample_group.analysis_result(depends_name).status != 'SUCCESS':
                return
        generic_task_body(sample_group, module, processor, sample_group)
    except UnsupportedAnalysisMode:
        pass
    try:
        processor = module.samples_processor()
        for depends_name in dependency_names:
            for sample in sample_group.samples:
                if sample.analysis_result(depends_name).status != 'SUCCESS':
                    return
        generic_task_body(sample_group, module, processor, sample_group.samples)
    except UnsupportedAnalysisMode:
        pass
