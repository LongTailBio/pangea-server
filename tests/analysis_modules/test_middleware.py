"""Test running middleware fully."""

import math

from analysis_packages.base.exceptions import UnsupportedAnalysisMode

from app.analysis_modules.wrangler import all_analysis_modules
from app.analysis_modules.task_graph import TaskConductor
from app.extensions import db

from ..utils import add_sample_group, add_sample
from .base import BaseAnalysisModuleTest
from .utils import unpack_module


SAMPLE_TEST_COUNT = 40


def processes_samples(analysis_module):
    """Return true if a module processes SampleToolResults."""
    try:
        # pylint: disable=assignment-from-no-return
        _ = analysis_module.group_tool_processor()
        return False
    except UnsupportedAnalysisMode:
        return True


def seed_samples(upstream, samples):
    """Create single sample."""
    factory = unpack_module(upstream)[2]
    for sample in samples:
        analysis_result = sample.analysis_result
        setattr(analysis_result, upstream.name(), factory.create_result())
        sample.save()


def numbered_sample(i=0, j=0):
    """Create numbered sample with metadata."""
    metadata = {'foobar': f'baz{j}'}
    sample = add_sample(f'Test Sample {i}', metadata=metadata)
    return sample


def seed_module(analysis_module, sample_group, samples):
    """Seed testing values for moduke."""
    upstream_modules = analysis_module.required_modules()
    for upstream in upstream_modules:
        if processes_samples(analysis_module):
            # Prepate Samples with ToolResults, if applicable
            seed_samples(upstream, samples)
        else:
            # Prepare GroupToolResult(s), if applicable
            factory = unpack_module(upstream)[2]
            tool_result = factory.create_result(save=False)
            tool_result.sample_group_uuid = sample_group.id
            tool_result.save()


class TestAnalysisModuleMiddleware(BaseAnalysisModuleTest):
    """Test running middleware fully."""

    pass


for module in all_analysis_modules:
    # Grab top-level values we need
    analysis_name = unpack_module(module)[1]

    def single_sample_test(self, analysis_module=module):
        """Test middleware for single Sample analyses."""
        sample = numbered_sample()
        if processes_samples(analysis_module):
            for tool in analysis_module.required_modules():
                seed_samples(tool, [sample])
        module_name = analysis_module.name()
        task_conductor = TaskConductor(str(sample.uuid), module_names=[module_name])
        task_signatures = task_conductor.build_task_signatures()
        analysis_task = task_signatures[0]
        analysis_task()

        analysis_result = sample.analysis_result.fetch()
        try:
            _ = analysis_module.single_sample_processor()
            self.assertIn(module_name, analysis_result)
        except UnsupportedAnalysisMode:
            self.assertNotIn(module_name, analysis_result)

    single_sample_test.__doc__ = f'Test {analysis_name} middleware for single Sample.'
    test_name = f'test_{analysis_name}_single_sample'
    setattr(TestAnalysisModuleMiddleware, test_name, single_sample_test)

    def sample_group_test(self, analysis_module=module):
        """Test middleware for SampleGroup analyses."""
        # Seed test values
        sample_group = add_sample_group('Test Group')
        meta_choices = [0, 1, 2]
        meta_choices = meta_choices * math.ceil(SAMPLE_TEST_COUNT / len(meta_choices))
        samples = [numbered_sample(i, meta_choices[i]) for i in range(SAMPLE_TEST_COUNT)]
        sample_group.samples = samples
        db.session.commit()
        seed_module(analysis_module, sample_group, samples)

        # Execute task
        module_name = analysis_module.name()
        task_conductor = TaskConductor(sample_group.id, module_names=[module_name], group=True)
        task_signatures = task_conductor.build_task_signatures()
        print(task_signatures)
        analysis_task = task_signatures[0]
        analysis_task()

        try:
            _ = analysis_module.single_sample_processor()
        except UnsupportedAnalysisMode:
            self.assertIn(module_name, sample_group.analysis_result)
            result = getattr(sample_group.analysis_result, module_name).fetch()
            self.assertEqual(result.status, 'S')
            self.assertIn('data', result)

    sample_group_test.__doc__ = f'Test {analysis_name} middleware SampleGroup.'
    test_name = f'test_{analysis_name}_sample_group'
    setattr(TestAnalysisModuleMiddleware, test_name, sample_group_test)
