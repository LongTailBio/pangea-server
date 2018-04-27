"""Test suite for KrakenHLL tool result model."""

from app.samples.sample_models import Sample
from app.tool_results.krakenhll import KrakenHLLResultModule, KrakenHLLResult
from app.tool_results.kraken.tests.constants import TEST_TAXA

from tests.base import BaseTestCase

KRAKENHLL_NAME = KrakenHLLResultModule.name()


class TestKrakenHLLModel(BaseTestCase):
    """Test suite for KrakenHLL tool result model."""

    def test_add_kraken_result(self):
        """Ensure KrakenHLL result model is created correctly."""
        sample_data = {'name': 'SMPL_01', KRAKENHLL_NAME: KrakenHLLResult(taxa=TEST_TAXA)}
        sample = Sample(**sample_data).save()
        self.assertTrue(hasattr(sample, KRAKENHLL_NAME))
        tool_result = getattr(sample, KRAKENHLL_NAME)
        self.assertEqual(len(tool_result.taxa), 6)
        self.assertEqual(tool_result.taxa['d__Viruses'], 1733)
        self.assertEqual(tool_result.taxa['d__Bacteria'], 7396285)
        self.assertEqual(tool_result.taxa['d__Archaea'], 12)
        self.assertEqual(tool_result.taxa['d__Bacteria|p__Proteobacteria'], 7285377)
        self.assertEqual(tool_result.taxa['d__Archaea|p__Euryarchaeota|c__Methanomicrobia'], 2)
        self.assertEqual(tool_result.taxa['d__Viruses|o__Caudovirales'], 1694)
