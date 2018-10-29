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


def processes_sample_groups(analysis_module):
    """Return true if a module processes SampleGroups"""
    try:
        # pylint: disable=assignment-from-no-return
        _ = analysis_module.samples_processor()
        return True
    except UnsupportedAnalysisMode:
        return False


def processes_single_samples(analysis_module):
    """Return true if a module processes single Samples"""
    try:
        # pylint: disable=assignment-from-no-return
        _ = analysis_module.single_sample_processor()
        return True
    except UnsupportedAnalysisMode:
        return False


def seed_sample(upstream, sample):
    """Create single sample."""
    factory = unpack_module(upstream)[2]
    analysis_result = sample.analysis_result
    setattr(analysis_result, upstream.name(), factory.create_result())
    sample.save()


def numbered_sample(i=0, j=0):
    """Create numbered sample with metadata."""
    metadata = {'foobar': f'baz{j}'}
    sample = add_sample(f'Test Sample {i}', metadata=metadata)
    return sample


def seed_module(analysis_module, sample_group):
    """Seed testing values for moduke."""
    upstream_modules = analysis_module.required_modules()
    for upstream in upstream_modules:
        for sample in sample_group.samples:
            seed_sample(upstream, sample)


def build_seeded_sample(analysis_module):
    """Return a sample with the given module's prereqs."""
    sample = numbered_sample()
    if processes_single_samples(analysis_module):
        for tool in analysis_module.required_modules():
            seed_sample(tool, sample)
    return sample


def build_seeded_sample_group(analysis_module):
    """Return a group with samples with the given modules prereqs."""
    sample_group = add_sample_group('Test Group')
    meta_choices = [0, 1, 2]
    meta_choices = meta_choices * math.ceil(SAMPLE_TEST_COUNT / len(meta_choices))
    samples = [numbered_sample(i, meta_choices[i]) for i in range(SAMPLE_TEST_COUNT)]
    sample_group.samples = samples
    db.session.commit()
    seed_module(analysis_module, sample_group)
    return sample_group


class TestAnalysisModuleMiddleware(BaseAnalysisModuleTest):
    """Test running middleware fully."""

    pass


for module in all_analysis_modules:
    # Grab top-level values we need
    analysis_name = unpack_module(module)[1]

    def single_sample_test(self, analysis_module=module):
        """Test middleware for single Sample analyses."""
        sample = build_seeded_sample(analysis_module)
        task_signatures = TaskConductor(
            str(sample.uuid), module_names=[analysis_module.name()]
        ).build_task_signatures()
        if not processes_single_samples(analysis_module):
            self.assertEqual(len(task_signatures), 0)
            return
        task_signatures[0].run()  # Modules are test one at a time so only one task present
        analysis_result = sample.analysis_result.fetch()
        self.assertIn(analysis_module.name(), analysis_result)

    single_sample_test.__doc__ = f'Test {analysis_name} middleware for single Sample.'
    test_name = f'test_{analysis_name}_single_sample'
    setattr(TestAnalysisModuleMiddleware, test_name, single_sample_test)

    def sample_group_test(self, analysis_module=module):
        """Test middleware for SampleGroup analyses."""
        sample_group = build_seeded_sample_group(analysis_module)
        task_signatures = TaskConductor(
            sample_group.id, module_names=[analysis_module.name()], group=True
        ).build_task_signatures()
        if not processes_sample_groups(analysis_module):
            self.assertEqual(len(task_signatures), 0)
            return
        task_signatures[0].run()  # Modules are test one at a time so only one task present
        self.assertIn(analysis_module.name(), sample_group.analysis_result)
        result = getattr(sample_group.analysis_result, analysis_module.name()).fetch()
        self.assertEqual(result.status, 'S')
        self.assertIn('data', result)

    sample_group_test.__doc__ = f'Test {analysis_name} middleware SampleGroup.'
    test_name = f'test_{analysis_name}_sample_group'
    setattr(TestAnalysisModuleMiddleware, test_name, sample_group_test)
