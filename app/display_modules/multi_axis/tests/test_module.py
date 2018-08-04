"""Test suite for Microbe Directory diplay module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.multi_axis import MultiAxisDisplayModule
from app.samples.sample_models import Sample
from app.display_modules.multi_axis.models import MultiAxisResult
from app.display_modules.multi_axis.constants import MODULE_NAME
from app.display_modules.multi_axis.tests.factory import MultiAxisFactory, create_values
from app.tool_results.card_amrs.tests import create_card_amr
from app.tool_results.humann2_normalize import create_humann2_normalize
from app.tool_results.krakenhll.tests import create_krakenhll
from app.tool_results.metaphlan2.tests import create_metaphlan2
from app.tool_results.microbe_census.tests import create_microbe_census


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
                **create_values(),
            ).save()

        self.generic_run_group_test(
            create_sample,
            MultiAxisDisplayModule
        )
