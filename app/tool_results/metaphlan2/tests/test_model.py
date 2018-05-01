"""Test suite for Metaphlan 2 tool result model."""

from app.samples.sample_models import Sample
from app.tool_results.metaphlan2 import Metaphlan2ResultModule, Metaphlan2Result
from app.tool_results.metaphlan2.tests.constants import TEST_TAXA

from tests.base import BaseTestCase


METAPHLAN2_NAME = Metaphlan2ResultModule.name()


class TestMetaphlan2Model(BaseTestCase):
    """Test suite for Metaphlan 2 tool result model."""

    def test_add_metaphlan2_result(self):
        """Ensure Metaphlan 2 result model is created correctly."""
        tool_result = Metaphlan2Result(taxa=TEST_TAXA).save()
        sample_data = {'name': 'SMPL_01', METAPHLAN2_NAME: tool_result}
        sample = Sample(**sample_data).save()
        self.assertTrue(hasattr(sample, METAPHLAN2_NAME))
        metaphlan_result = getattr(sample, METAPHLAN2_NAME).fetch()
        self.assertEqual(len(metaphlan_result.taxa), 6)
        self.assertEqual(metaphlan_result.taxa['d__Viruses'], 1733)
        self.assertEqual(metaphlan_result.taxa['d__Bacteria'], 7396285)
        self.assertEqual(metaphlan_result.taxa['d__Archaea'], 12)
        self.assertEqual(metaphlan_result.taxa['d__Bacteria|p__Proteobacteria'], 7285377)
        self.assertEqual(metaphlan_result.taxa['d__Archaea|p__Euryarchaeota|c__Methanomicrobia'], 2)
        self.assertEqual(metaphlan_result.taxa['d__Viruses|o__Caudovirales'], 1694)
