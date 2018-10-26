"""Test suite for Average Genome Size analysis."""

from unittest import TestCase

from mongoengine import ValidationError
from ..models import DistributionResult


class TestAverageGenomeSizeModels(TestCase):
    """Test suite for Average Genome Size analysis."""

    def test_add_unordered_distribution(self):
        """Ensure saving model fails if distribution record is unordered."""
        distribution = DistributionResult(min_val=4, q1_val=1, mean_val=2,
                                          q3_val=3, max_val=0)
        self.assertRaises(ValidationError, distribution.validate)
