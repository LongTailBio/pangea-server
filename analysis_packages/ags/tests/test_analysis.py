"""Test suite for Average Genome Size tasks."""

from unittest import TestCase

from tool_packages.microbe_census.tests.factory import create_values

from ..analysis import ags_distributions


class TestAverageGenomeSizeTasks(TestCase):
    """Test suite for Average Genome Size tasks."""

    def test_ags_distributions(self):
        """Ensure ags_distributions task works."""

        def create_sample(i):
            """Create test sample."""
            metadata = {'foo': f'bar{i}'}
            sample = {
                'name': f'SMPL_{i}',
                'metadata': metadata,
                'microbe_census': create_values(),
            }
            return sample

        samples = [create_sample(i) for i in range(15)]
        result = ags_distributions(samples)
        self.assertIn('foo', result)
        self.assertIn('bar0', result['foo'])
        self.assertIn('bar1', result['foo'])
        self.assertIn('min_val', result['foo']['bar0'])
