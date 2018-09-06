"""Test suite for Functional Genes diplay module."""

from tool_packages.humann2_normalize.tests.factory import create_result

from app.display_modules.display_module_base_test import (
    BaseDisplayModuleTest,
    generic_create_sample,
)
from app.display_modules.functional_genes import FunctionalGenesDisplayModule
from app.display_modules.functional_genes import FunctionalGenesResult
from app.display_modules.functional_genes.constants import MODULE_NAME, TOOL_MODULE_NAME
from app.display_modules.functional_genes.tests.factory import FunctionalGenesFactory
from app.display_modules.generic_gene_set.tests.factory import create_one_sample


class TestFunctionalGenesModule(BaseDisplayModuleTest):
    """Test suite for FunctionalGenes diplay module."""

    def test_get_functional_genes(self):
        """Ensure getting a single Functional Genes behaves correctly."""
        func_genes = FunctionalGenesFactory()
        self.generic_getter_test(func_genes, MODULE_NAME)

    def test_add_functional_genes(self):
        """Ensure FunctionalGenes model is created correctly."""
        samples = {
            'test_sample_1': create_one_sample(),
            'test_sample_2': create_one_sample(),
        }
        func_genes_result = FunctionalGenesResult(samples=samples)
        self.generic_adder_test(func_genes_result, MODULE_NAME)

    def test_run_functional_genes_sample_group(self):  # pylint: disable=invalid-name
        """Ensure Functional Genes run_sample_group produces correct result."""
        create_sample = generic_create_sample(TOOL_MODULE_NAME, create_result)
        self.generic_run_group_test(create_sample,
                                    FunctionalGenesDisplayModule)
