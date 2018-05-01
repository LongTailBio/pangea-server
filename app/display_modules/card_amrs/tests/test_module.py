"""Test suite for CARD Genes diplay module."""

from app.display_modules.card_amrs import CARDGenesDisplayModule
from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.card_amrs import CARDGenesResult
from app.display_modules.card_amrs.constants import MODULE_NAME
from app.display_modules.card_amrs.tests.factory import CARDGenesFactory
from app.display_modules.generic_gene_set.tests.factory import create_one_sample
from app.samples.sample_models import Sample
from app.tool_results.card_amrs.tests.factory import create_card_amr
from app.tool_results.card_amrs.constants import MODULE_NAME as TOOL_MODULE_NAME


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

        def create_sample(i):
            """Create unique sample for index i."""
            args = {
                'name': f'Sample{i}',
                'metadata': {'foobar': f'baz{i}'},
                TOOL_MODULE_NAME: create_card_amr(),
            }
            return Sample(**args).save()

        self.generic_run_group_test(create_sample,
                                    CARDGenesDisplayModule)
