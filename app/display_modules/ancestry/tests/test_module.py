"""Test suite for Ancestry diplay module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.ancestry.wrangler import AncestryWrangler
from app.samples.sample_models import Sample
from app.display_modules.ancestry.models import AncestryResult
from app.display_modules.ancestry.constants import MODULE_NAME, TOOL_MODULE_NAME
from app.display_modules.ancestry.tests.factory import AncestryFactory
from app.tool_results.ancestry.tests.factory import (
    create_values,
    create_ancestry
)


class TestAncestryModule(BaseDisplayModuleTest):
    """Test suite for Ancestry diplay module."""

    def test_get_ancestry(self):
        """Ensure getting a single Ancestry behaves correctly."""
        ancestry = AncestryFactory()
        self.generic_getter_test(ancestry, MODULE_NAME)

    def test_add_ancestry(self):
        """Ensure Ancestry model is created correctly."""
        samples = {
            'sample_1': create_values(),
            'sample_2': create_values(),
        }
        ancestry_result = AncestryResult(samples=samples)
        self.generic_adder_test(ancestry_result, MODULE_NAME)

    def test_run_ancestry_sample(self):  # pylint: disable=invalid-name
        """Ensure TaxaTree run_sample produces correct results."""
        kwargs = {
            TOOL_MODULE_NAME: create_ancestry(),
        }
        self.generic_run_sample_test(kwargs, AncestryWrangler, MODULE_NAME)

    def test_run_ancestry_sample_group(self):  # pylint: disable=invalid-name
        """Ensure Ancestry run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_ancestry()
            args = {
                'name': f'Sample{i}',
                'metadata': {'foobar': f'baz{i}'},
                TOOL_MODULE_NAME: data,
            }
            return Sample(**args).save()

        self.generic_run_group_test(create_sample,
                                    AncestryWrangler,
                                    MODULE_NAME)
