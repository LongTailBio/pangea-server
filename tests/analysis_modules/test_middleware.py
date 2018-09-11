"""Test running middleware fully."""

from analysis_packages.ags import AGSAnalysisModule
from analysis_packages.base.exceptions import UnsupportedAnalysisMode

from app.analysis_modules.utils import conduct_sample, conduct_sample_group
from app.extensions import db

from ..tool_results.utils import unpack_module as unpack_tool
from ..utils import add_sample_group, add_sample
from .base import BaseAnalysisModuleTest


def processes_samples(module):
    """Return true if a module processes SampleToolResults."""
    try:
        # pylint: disable=assignment-from-no-return
        _ = module.group_tool_processor()
        return False
    except UnsupportedAnalysisMode:
        return True


def seed_samples(module, samples):
    """Create single sample."""
    tool_modules = module.required_tool_results()
    for tool in tool_modules:
        name = tool.name()
        factory = unpack_tool(tool)[2]
        for sample in samples:
            setattr(sample, name, factory.create_result())
            sample.save()


def numbered_sample(i):
    """Create numbered sample with metadata."""
    metadata = {'foobar': f'baz{i}'}
    sample = add_sample(f'Test Sample {i}', metadata=metadata)
    return sample


def seed_module(module, sample_group, samples):
    """Seed testing values for moduke."""
    if processes_samples(module):
        # Prepate Samples with ToolResults, if applicable
        seed_samples(module, samples)
    else:
        # Prepare GroupToolResult(s), if applicable
        factory = unpack_tool(module)[2]
        tool_result = factory.create_result(save=False)
        tool_result.sample_group_uuid = sample_group.id
        tool_result.save()


class TestAnalysisModuleMiddleware(BaseAnalysisModuleTest):
    """Test running middleware fully."""

    def test_single_sample(self):
        """Test middleware for single Sample analyses."""
        analysis_module = AGSAnalysisModule

        sample = numbered_sample(0)
        seed_samples(analysis_module, [sample])
        module_name = analysis_module.name()
        task_signatures = conduct_sample(str(sample.uuid), [module_name])
        ags_task = task_signatures[0]
        ags_task()

        analysis_result = sample.analysis_result.fetch()
        self.assertNotIn(module_name, analysis_result)

    def test_sample_group(self):
        """Test middleware for SampleGroup analyses."""
        analysis_module = AGSAnalysisModule

        # Seed test values
        sample_group = add_sample_group('Test Group')
        samples = [numbered_sample(i) for i in range(5)]
        sample_group.samples = samples
        db.session.commit()
        seed_module(analysis_module, sample_group, samples)

        # Execute task
        module_name = analysis_module.name()
        task_signatures = conduct_sample_group(sample_group.id, [module_name])
        ags_task = task_signatures[0]
        ags_task()

        if processes_samples(analysis_module):
            self.assertIn(module_name, sample_group.analysis_result)
            result = getattr(sample_group.analysis_result, module_name).fetch()
        else:
            model = analysis_module.result_model()
            result = model.objects.get(sample_group_uuid=sample_group.id)
        self.assertEqual(result.status, 'S')
        self.assertIn('data', result)
