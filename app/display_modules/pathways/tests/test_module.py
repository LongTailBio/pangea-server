"""Test suite for Pathway display module."""
from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.pathways import PathwaysDisplayModule
from app.display_modules.pathways.models import PathwayResult
from app.display_modules.pathways.constants import MODULE_NAME
from app.display_modules.pathways.tests.factory import (
    PathwayFactory,
    create_one_sample,
)
from app.samples.sample_models import Sample
from app.tool_results.humann2.tests.factory import create_humann2


class TestPathwaysModule(BaseDisplayModuleTest):
    """Test suite for Pathway diplay module."""

    def test_get_pathway(self):
        """Ensure getting a single Pathway behaves correctly."""
        paths = PathwayFactory()
        self.generic_getter_test(paths, MODULE_NAME)

    def test_add_pathway(self):
        """Ensure Pathway model is created correctly."""
        samples = {
            'test_sample_1': create_one_sample(),
            'test_sample_2': create_one_sample(),
        }
        humann2_result = PathwayResult(samples=samples)
        self.generic_adder_test(humann2_result, MODULE_NAME)

    def test_run_pathway_sample_group(self):  # pylint: disable=invalid-name
        """Ensure Pathway run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_humann2()
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          humann2_functional_profiling=data).save()

        self.generic_run_group_test(create_sample,
                                    PathwaysDisplayModule)
