"""Test suite for Alpha Diversity diplay module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.alpha_div import (
    AlphaDivWrangler,
    AlphaDiversityResult,
    MODULE_NAME,
)
from app.samples.sample_models import Sample
from app.tool_results.alpha_diversity.tests.factory import (
    create_alpha_diversity,
)

from .factory import AlphaDivFactory, create_categories, create_tools, create_by_tool


class TestAlphaDivModule(BaseDisplayModuleTest):
    """Test suite for Alpha Diversity diplay module."""

    def test_add_alpha_div(self):
        """Ensure Alpha Diversity model is created correctly."""
        packed_data = {
            'categories': create_categories(),
            'tool_names': create_tools(),
        }
        packed_data['by_tool'] = create_by_tool(packed_data)
        alpha_div_result = AlphaDiversityResult(**packed_data)
        self.generic_adder_test(alpha_div_result, MODULE_NAME)

    def test_get_alpha_div(self):
        """Ensure getting a single Alpha Diversity behaves correctly."""
        alpha_diversity = AlphaDivFactory()
        fields = ('categories', 'tool_names', 'by_tool')
        self.generic_getter_test(alpha_diversity, MODULE_NAME, verify_fields=fields)

    def test_run_alpha_div_sample_group(self):  # pylint: disable=invalid-name
        """Ensure Alpha Diversity run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_alpha_diversity()
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          alpha_diversity_stats=data).save()

        self.generic_run_group_test(create_sample,
                                    AlphaDivWrangler,
                                    MODULE_NAME)
