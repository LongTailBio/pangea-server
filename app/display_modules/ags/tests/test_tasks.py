"""Test suite for Average Genome Size tasks."""

from tool_packages.microbe_census.tests.factory import create_result as create_microbe_census

from app.display_modules.ags.ags_tasks import boxplot, ags_distributions
from app.samples.sample_models import Sample

from tests.base import BaseTestCase


class TestAverageGenomeSizeTasks(BaseTestCase):
    """Test suite for Average Genome Size tasks."""

    def test_boxplot(self):
        """Ensure boxplot method creates correct boxplot."""
        values = [37, 48, 30, 53, 3, 83, 19, 71, 90, 16, 19, 7, 11, 43, 43]
        result = boxplot(values)
        self.assertEqual(3, result['min_val'])
        self.assertEqual(17.5, result['q1_val'])
        self.assertEqual(37, result['mean_val'])
        self.assertEqual(50.5, result['q3_val'])
        self.assertEqual(90, result['max_val'])

    def test_ags_distributions(self):
        """Ensure ags_distributions task works."""

        def create_sample(i):
            """Create test sample."""
            metadata = {'foo': f'bar{i}'}
            return Sample(name=f'SMPL_{i}',
                          metadata=metadata,
                          microbe_census=create_microbe_census())

        samples = [create_sample(i).fetch_safe() for i in range(15)]
        result = ags_distributions.delay(samples).get()
        self.assertIn('foo', result)
        self.assertIn('bar0', result['foo'])
        self.assertIn('bar1', result['foo'])
        self.assertIn('min_val', result['foo']['bar0'])
