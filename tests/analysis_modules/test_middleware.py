"""Test running middleware fully."""

from analysis_packages.ags import AGSAnalysisModule
from analysis_packages.base.exceptions import UnsupportedAnalysisMode

from app.analysis_modules.utils import conduct_sample, conduct_sample_group
from app.extensions import db

from ..tool_results.utils import unpack_module as unpack_tool
from ..utils import add_sample_group, add_sample
from .base import BaseAnalysisModuleTest


def sample_factory(analysis_module, i):
    """Create single sample."""
    metadata = {'foobar': f'baz{i}'}
    sample = add_sample(f'Test Sample {i}', metadata=metadata)
    tool_modules = analysis_module.required_tool_results()
    for tool in tool_modules:
        name = tool.name()
        factory = unpack_tool(tool)[2]
        setattr(sample, name, factory.create_result())
    sample.save()
    return sample


class TestAnalysisModuleMiddleware(BaseAnalysisModuleTest):
    """Test running middleware fully."""

    def test_single_ags(self):
        """Test middleware for Average Genome Size."""
        analysis_module = AGSAnalysisModule

        sample = sample_factory(analysis_module, 0)
        module_name = analysis_module.name()
        task_signatures = conduct_sample(str(sample.uuid), [module_name])
        ags_task = task_signatures[0]
        ags_task()

        analysis_result = sample.analysis_result.fetch()
        self.assertNotIn(module_name, analysis_result)

    def test_group_ags(self):
        """Test middleware for Average Genome Size."""
        analysis_module = AGSAnalysisModule
        sample_group = add_sample_group('Test Group')

        # Prepate Samples with ToolResults, if applicable
        try:
            _ = analysis_module.samples_processor()
            samples = [sample_factory(analysis_module, i) for i in range(5)]
            sample_group.samples = samples
            db.session.commit()
        except UnsupportedAnalysisMode:
            pass

        # Prepare GroupToolResult(s), if applicable
        try:
            # pylint: disable=assignment-from-no-return
            _ = analysis_module.group_tool_processor()
            for tool in analysis_module.required_tool_results():
                factory = unpack_tool(tool)[2]
                tool_result = factory.create_result(save=False)
                tool_result.sample_group_uuid = sample_group.id
                tool_result.save()
        except UnsupportedAnalysisMode:
            pass

        module_name = analysis_module.name()
        task_signatures = conduct_sample_group(sample_group.id, [module_name])
        ags_task = task_signatures[0]
        ags_task()

        self.assertIn(module_name, sample_group.analysis_result)
        ags_result = getattr(sample_group.analysis_result, module_name).fetch()
        self.assertEqual(ags_result.status, 'S')
        self.assertIn('data', ags_result)
