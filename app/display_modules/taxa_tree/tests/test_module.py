"""Test suite for Taxa Tree display module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.taxa_tree.wrangler import TaxaTreeWrangler
from app.display_modules.taxa_tree.models import TaxaTreeResult
from app.display_modules.taxa_tree.constants import MODULE_NAME
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.kraken.tests.factory import create_kraken
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.krakenhll.tests.factory import create_krakenhll
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.metaphlan2.tests.factory import create_metaphlan2

from .factory import generate_random_tree, TaxaTreeFactory


class TestTaxaTreeModule(BaseDisplayModuleTest):
    """Test suite for TaxaTree display module."""

    def test_get_taxa_tree(self):
        """Ensure getting a single TaxaTree behaves correctly."""
        ttree = TaxaTreeFactory()
        self.generic_getter_test(ttree, MODULE_NAME,
                                 verify_fields=('metaphlan2', 'kraken', 'krakenhll'))

    def test_add_taxa_tree(self):
        """Ensure TaxaTree model is created correctly."""
        kwargs = {
            'metaphlan2': generate_random_tree(),
            'kraken': generate_random_tree(),
            'krakenhll': generate_random_tree(),
        }
        taxa_tree_result = TaxaTreeResult(**kwargs)
        self.generic_adder_test(taxa_tree_result, MODULE_NAME)

    def test_run_taxa_tree_sample(self):  # pylint: disable=invalid-name
        """Ensure TaxaTree run_sample produces correct results."""
        kwargs = {
            KrakenResultModule.name(): create_kraken(),
            KrakenHLLResultModule.name(): create_krakenhll(),
            Metaphlan2ResultModule.name(): create_metaphlan2(),
        }
        self.generic_run_sample_test(kwargs, TaxaTreeWrangler, MODULE_NAME)
