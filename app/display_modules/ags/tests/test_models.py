"""Test suite for Average Genome Size model."""

from mongoengine import ValidationError

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.ags.ags_models import AGSResult, DistributionResult

from tests.base import BaseTestCase


CATEGORIES = {'foo': ['bar', 'baz']}
DISTRIBUTIONS = {
    'foo': {
        'bar': DistributionResult(min_val=0, q1_val=1, mean_val=2,
                                  q3_val=3, max_val=4),
        'baz': DistributionResult(min_val=5, q1_val=6, mean_val=7,
                                  q3_val=8, max_val=9),
    },
}


class TestAverageGenomeSizeResult(BaseTestCase):
    """Test suite for Average Genome Size model."""

    def test_add_ags(self):
        """Ensure Average Genome Size model is created correctly."""
        ags = AGSResult(categories=CATEGORIES, distributions=DISTRIBUTIONS)
        wrapper = AnalysisResultWrapper(data=ags).save()
        result = AnalysisResultMeta(average_genome_size=wrapper).save()
        self.assertTrue(result.id)
        self.assertTrue(result.average_genome_size)

    def test_add_unordered_distribution(self):
        """Ensure saving model fails if distribution record is unordered."""
        unordered_distributions = DISTRIBUTIONS.copy()
        bad_distribution = DistributionResult(min_val=4, q1_val=1, mean_val=2,
                                              q3_val=3, max_val=0)
        unordered_distributions['foo']['bar'] = bad_distribution
        ags = AGSResult(categories=CATEGORIES, distributions=unordered_distributions)
        wrapper = AnalysisResultWrapper(data=ags)
        self.assertRaises(ValidationError, wrapper.save)
