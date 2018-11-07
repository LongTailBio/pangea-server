"""Test suite for Microbe Census tool result model."""

from unittest import TestCase

from mongoengine import ValidationError

from .. import MicrobeCensusResult
from .constants import TEST_CENSUS


class TestMicrobeCensusResultModel(TestCase):
    """Test suite for Microbe Census tool result model."""

    def test_add_result_missing_fields(self):
        """Ensure validation fails if missing field."""
        partial_microbe_census = dict(TEST_CENSUS)
        partial_microbe_census.pop('average_genome_size', None)
        microbe_census = MicrobeCensusResult(**partial_microbe_census)
        self.assertRaises(ValidationError, microbe_census.validate)

    def test_add_negative_value(self):
        """Ensure validation fails for negative values."""
        bad_microbe_census = dict(TEST_CENSUS)
        bad_microbe_census['average_genome_size'] = -3
        microbe_census = MicrobeCensusResult(**bad_microbe_census)
        self.assertRaises(ValidationError, microbe_census.validate)
