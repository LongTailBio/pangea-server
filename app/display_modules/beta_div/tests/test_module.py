"""Test suite for Beta Diversity display module."""

from tool_packages.beta_diversity.models import BetaDiversityToolResult
from tool_packages.beta_diversity.tests.factory import create_values

from app.display_modules.beta_div import BetaDiversityDisplayModule
from app.display_modules.beta_div.models import BetaDiversityResult
from app.display_modules.beta_div import MODULE_NAME
from app.display_modules.display_module_base_test import BaseDisplayModuleTest

from tests.utils import add_sample_group

from .factory import BetaDiversityFactory


class TestBetaDivModule(BaseDisplayModuleTest):
    """Test suite for Beta Diversity diplay module."""

    def test_add_beta_div(self):
        """Ensure Beta Diversity model is created correctly."""
        ranks = create_values()
        beta_div_result = BetaDiversityResult(data=ranks)
        self.generic_adder_test(beta_div_result, MODULE_NAME)

    def test_get_beta_div(self):
        """Ensure getting a single Beta Diversity behaves correctly."""
        beta_div_result = BetaDiversityFactory()
        self.generic_getter_test(beta_div_result, MODULE_NAME,
                                 verify_fields=('data',))

    def test_run_beta_div_sample_group(self):  # pylint: disable=invalid-name
        """Ensure Beta Diversity run_sample_group produces correct results."""

        def create_sample_group():
            """Create unique sample for index i."""
            sample_group = add_sample_group(name='SampleGroup01')
            ranks = create_values()
            BetaDiversityToolResult(sample_group_uuid=sample_group.id, data=ranks).save()
            return sample_group

        self.generic_run_group_test(None,
                                    BetaDiversityDisplayModule,
                                    group_builder=create_sample_group)
