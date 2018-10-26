"""Test suite for Average Genome Size model."""

from unittest import TestCase

from mongoengine import ValidationError
from analysis_packages.base.models import DistributionResult

from ..models import AGSResult


class TestAverageGenomeSizeResult(TestCase):
    """Test suite for Average Genome Size model."""

    def test_add_ags(self):
        """Ensure Average Genome Size model is created correctly."""
        categories = {'foo': ['bar', 'baz']}
        distributions = {
            'foo': {
                'bar': DistributionResult(min_val=0, q1_val=1, mean_val=2,
                                          q3_val=3, max_val=4),
                'baz': DistributionResult(min_val=5, q1_val=6, mean_val=7,
                                          q3_val=8, max_val=9),
            },
        }
        ags = AGSResult(categories=categories, distributions=distributions)
        try:
            ags.validate()
        except ValidationError:
            self.fail('AGSResult validation raised unexpected ValidationError.')
