"""Test suite for CARD Genes diplay module."""

from tool_packages.card_amrs.tests.factory import create_result
from tool_packages.card_amrs.constants import MODULE_NAME as TOOL_MODULE_NAME

from app.display_modules.card_amrs import CARDGenesDisplayModule, CARDGenesResult
from app.display_modules.card_amrs.constants import MODULE_NAME
from app.display_modules.card_amrs.tests.factory import CARDGenesFactory
from app.display_modules.generic_gene_set.tests.factory import create_one_sample

from app.display_modules.display_module_base_test import (
    BaseDisplayModuleTest,
    generic_create_sample,
)


class TestCARDGenesModule(BaseDisplayModuleTest):
    """Test suite for CARD Genes diplay module."""

    def test_get_card_genes(self):
        """Ensure getting a single CARD Genes behaves correctly."""
        card_amrs = CARDGenesFactory()
        self.generic_getter_test(card_amrs, MODULE_NAME)

    def test_add_card_genes(self):
        """Ensure CARD Genes model is created correctly."""
        samples = {
            'test_sample_1': create_one_sample(),
            'test_sample_2': create_one_sample(),
        }
        card_amr_result = CARDGenesResult(samples=samples)
        self.generic_adder_test(card_amr_result, MODULE_NAME)

    def test_run_card_genes_sample_group(self):  # pylint: disable=invalid-name
        """Ensure CARD Genes run_sample_group produces correct results."""
        create_sample = generic_create_sample(TOOL_MODULE_NAME, create_result)
        self.generic_run_group_test(create_sample,
                                    CARDGenesDisplayModule)
