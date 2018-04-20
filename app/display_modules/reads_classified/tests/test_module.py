"""Test suite for Reads Classified display module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.reads_classified.wrangler import ReadsClassifiedWrangler
from app.display_modules.reads_classified.models import ReadStatsResult
from app.display_modules.reads_classified.constants import MODULE_NAME, TOOL_MODULE_NAME
from app.display_modules.reads_classified.tests.factory import ReadStatsFactory
from app.samples.sample_models import Sample
from app.tool_results.reads_classified.tests.factory import (
    create_read_stats,
    create_values
)


class TestReadsClassifiedModule(BaseDisplayModuleTest):
    """Test suite for ReadsClassified diplay module."""

    def test_get_reads_classified(self):
        """Ensure getting a single ReadsClassified behaves correctly."""
        reads_class = ReadsClassifiedFactory()
        self.generic_getter_test(reads_class, MODULE_NAME)

    def test_add_reads_classified(self):
        """Ensure ReadsClassified model is created correctly."""
        samples = {
            'test_sample_1': create_values(),
            'test_sample_2': create_values(),
        }
        read_class_result = ReadsClassifiedResult(samples=samples)
        self.generic_adder_test(read_class_result, MODULE_NAME)

    def test_run_reads_classified_sample_group(self):  # pylint: disable=invalid-name
        """Ensure ReadsClassified run_sample_group produces correct results."""
        def create_sample(i):
            """Create unique sample for index i."""
            args = {
                'name': f'Sample{i}',
                'metadata': {'foobar': f'baz{i}'},
                TOOL_MODULE_NAME: create_read_stats(),
            }
            return Sample(**args).save()

        self.generic_run_group_test(create_sample,
                                    ReadsClassifiedWrangler,
                                    MODULE_NAME)
