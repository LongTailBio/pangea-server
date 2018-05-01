"""Test suite for ReadStats display module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.read_stats import ReadStatsDisplayModule
from app.display_modules.read_stats.models import ReadStatsResult
from app.display_modules.read_stats.constants import MODULE_NAME
from app.display_modules.read_stats.tests.factory import ReadStatsFactory
from app.samples.sample_models import Sample
from app.tool_results.read_stats.tests.factory import (
    create_read_stats,
    create_values
)


class TestReadStatsModule(BaseDisplayModuleTest):
    """Test suite for ReadStats diplay module."""

    def test_get_read_stats(self):
        """Ensure getting a single ReadStats behaves correctly."""
        rstats = ReadStatsFactory()
        self.generic_getter_test(rstats, MODULE_NAME)

    def test_add_read_stats(self):
        """Ensure ReadStats model is created correctly."""
        samples = {
            'test_sample_1': create_values(),
            'test_sample_2': create_values(),
        }
        read_stats_result = ReadStatsResult(samples=samples)
        self.generic_adder_test(read_stats_result, MODULE_NAME)

    def test_run_read_stats_sample_group(self):  # pylint: disable=invalid-name
        """Ensure ReadStats run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_read_stats()
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          read_stats=data).save()

        self.generic_run_group_test(create_sample,
                                    ReadStatsDisplayModule)
