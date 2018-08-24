"""Tasks for the Conductor module."""

from flask import current_app

from app.analysis_modules import all_analysis_modules
from app.extensions import celery
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results import all_tool_results


@celery.task()
def fetch_samples(sample_group_id):
    """Get all samples belonging to the specified Sample Group."""
    sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
    samples = [sample.fetch_safe() for sample in sample_group.samples]
    return samples


@celery.task()
def filter_samples(samples, module_name):
    """Filter list of samples to only those supporting the given module."""
    module = [module for module in all_analysis_modules
              if module.name() is module_name][0]
    dependencies = set([tool.name() for tool in module.required_tool_results()])

    def test_sample(sample):
        """Test a single sample to see if it has all tools required by the display module."""
        all_fields = [mod.name() for mod in all_tool_results]
        tools_present = set([field for field in all_fields
                             if sample.get(field, None) is not None])
        is_valid = dependencies <= tools_present
        sample_name = sample['name']
        current_app.logger.debug(f'Testing sample: {sample_name}')
        current_app.logger.debug(f'Tools present: {tools_present}')
        current_app.logger.debug(f'Is valid: {is_valid}')
        return is_valid

    result = [sample for sample in samples if test_sample(sample)]
    current_app.logger.debug(f'result: {result}')
    return result
