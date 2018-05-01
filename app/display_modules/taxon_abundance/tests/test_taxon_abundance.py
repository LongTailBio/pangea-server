"""Test suite for Taxon Abundance model."""

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.taxon_abundance import TaxonAbundanceResult
from app.display_modules.taxon_abundance.constants import MODULE_NAME
from app.display_modules.taxon_abundance import TaxonAbundanceDisplayModule
from app.samples.sample_models import Sample
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.krakenhll.tests.factory import create_krakenhll
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.kraken.tests.factory import create_kraken
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.metaphlan2.tests.factory import create_metaphlan2


def flow_model():
    """Return an example flow model."""
    return {
        'nodes': [
            {
                'id': 'left_root',
                'name': 'left_root',
                'value': 3.5,
                'rank': 'l',
            },
            {
                'id': 'right_root',
                'name': 'right_root',
                'value': 3.5,
                'rank': 'r',
            },
        ], 'edges': [
            {
                'source': 'left_root',
                'target': 'right_root',
                'value': 1.0,
            },
        ]
    }


class TestTaxonAbundanceResult(BaseDisplayModuleTest):
    """Test suite for Taxon Abundance model."""

    def test_add_taxon_abundance(self):
        """Ensure Taxon Abundance model is created correctly."""
        taxon_abundance = TaxonAbundanceResult(**{
            'by_tool': {
                'kraken': flow_model(),
                'metaphlan2': flow_model()
            }
        })
        wrapper = AnalysisResultWrapper(data=taxon_abundance)
        result = AnalysisResultMeta(taxon_abundance=wrapper).save()
        self.assertTrue(result.id)
        self.assertTrue(result.taxon_abundance)

    def test_get_taxon_abundance(self):
        """Ensure getting a single TaxonAbundance behaves correctly."""
        taxon_abundance = TaxonAbundanceResult(**{
            'by_tool': {
                'kraken': flow_model(),
                'metaphlan2': flow_model()
            }
        })
        self.generic_getter_test(taxon_abundance, MODULE_NAME,
                                 verify_fields=('by_tool',))

    def test_run_taxon_abundance_sample_group(self):  # pylint: disable=invalid-name
        """Ensure TaxonAbundance run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            return Sample(**{
                'name': f'Sample{i}',
                'metadata': {'foobar': f'baz{i}'},
                KrakenResultModule.name(): create_kraken(),
                KrakenHLLResultModule.name(): create_krakenhll(),
                Metaphlan2ResultModule.name(): create_metaphlan2(),
            }).save()

        self.generic_run_group_test(create_sample,
                                    TaxonAbundanceDisplayModule)
