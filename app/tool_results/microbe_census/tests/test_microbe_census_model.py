"""Test suite for Microbe Census tool result model."""

from mongoengine import ValidationError

from app.samples.sample_models import Sample
from app.tool_results.microbe_census import MicrobeCensusResult
from app.tool_results.microbe_census.tests.constants import TEST_CENSUS

from tests.base import BaseTestCase


class TestMicrobeCensusResultModel(BaseTestCase):
    """Test suite for Microbe Census tool result model."""

    def test_add_hmp_sites_result(self):
        """Ensure Microbe Census result model is created correctly."""
        microbe_census = MicrobeCensusResult(**TEST_CENSUS).save()
        sample = Sample(name='SMPL_01', microbe_census=microbe_census).save()
        self.assertTrue(sample.microbe_census)
        tool_result = sample.microbe_census.fetch()
        self.assertEqual(tool_result['average_genome_size'], 3)
        self.assertEqual(tool_result['total_bases'], 5)
        self.assertEqual(tool_result['genome_equivalents'], 250)

    def test_add_result_missing_fields(self):
        """Ensure validation fails if missing field."""
        partial_microbe_census = dict(TEST_CENSUS)
        partial_microbe_census.pop('average_genome_size', None)
        microbe_census = MicrobeCensusResult(**partial_microbe_census)
        self.assertRaises(ValidationError, microbe_census.save)

    def test_add_negative_value(self):
        """Ensure validation fails for negative values."""
        bad_microbe_census = dict(TEST_CENSUS)
        bad_microbe_census['average_genome_size'] = -3
        microbe_census = MicrobeCensusResult(**bad_microbe_census)
        self.assertRaises(ValidationError, microbe_census.save)
