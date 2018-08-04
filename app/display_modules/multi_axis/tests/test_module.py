"""Test suite for Microbe Directory diplay module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.multi_axis import MultiAxisDisplayModule
from app.samples.sample_models import Sample
from app.display_modules.multi_axis.models import MultiAxisResult
from app.display_modules.multi_axis.constants import MODULE_NAME
from app.display_modules.multi_axis.tests.factory import MultiAxisFactory
from app.tool_results.multi_axis.tests.factory import (
    create_values,
    create_taxa,
    create_genes,
    create_ags,
)


class TestMultiAxisModule(BaseDisplayModuleTest):
    """Test suite for Microbe Directory diplay module."""

    def test_get_multi_axis(self):
        """Ensure getting a single MultiAxis behaves correctly."""
        multi_axis = MultiAxisFactory()
        self.generic_getter_test(multi_axis, MODULE_NAME)

    def test_add_multi_axis(self):
        """Ensure MultiAxis model is created correctly."""
        samples = {
            'sample_1': create_values(),
            'sample_2': create_values(),
        }
        multi_axis_result = MultiAxisResult(samples=samples)
        self.generic_adder_test(multi_axis_result, MODULE_NAME)

    def test_run_multi_axis_sample_group(self):  # pylint: disable=invalid-name
        """Ensure microbe directory run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            return Sample(
                name=f'Sample{i}',
                metadata={'foobar': f'baz{i}'},
                metaphlan2_taxonomy_profiling=create_taxa(),
                krakenhll_taxonomy_profiling=create_taxa(),
                align_to_amr_genes=create_genes(),
                humann2_normalize_genes=create_genes(),
                microbe_census=create_ags(),
            ).save()

        self.generic_run_group_test(
            create_sample,
            MultiAxisDisplayModule
        )
