"""Test suite for Average Genome Size analysis."""

from unittest import TestCase

from ..utils import boxplot


class TestAverageGenomeSizeTasks(TestCase):
    """Test suite for Average Genome Size analysis."""

    def test_boxplot(self):
        """Ensure boxplot method creates correct boxplot."""
        values = [37, 48, 30, 53, 3, 83, 19, 71, 90, 16, 19, 7, 11, 43, 43]
        result = boxplot(values)
        self.assertEqual(3, result['min_val'])
        self.assertEqual(17.5, result['q1_val'])
        self.assertEqual(37, result['mean_val'])
        self.assertEqual(50.5, result['q3_val'])
        self.assertEqual(90, result['max_val'])
