"""Test suite for AnalysisModule utility tasks."""

from unittest import TestCase

from tool_packages.kraken import KrakenResultModule
from tool_packages.kraken.tests.factory import create_result as create_kraken

from analysis_packages.base.utils import (
    categories_from_metadata,
    collate_samples,
)


KRAKEN_NAME = KrakenResultModule.name()


class TestDisplayModuleUtilityTasks(TestCase):
    """Test suite for Display Module utility tasks."""

    def test_categories_from_metadata(self):
        """Ensure categories_from_metadata task works."""
        metadata1 = {
            'valid_category': 'foo',
            'invalid_category': 'bar',
        }
        metadata2 = {
            'valid_category': 'baz',
        }
        sample1 = {'name': 'Sample01', 'metadata': metadata1}
        sample2 = {'name': 'Sample02', 'metadata': metadata2}
        result = categories_from_metadata([sample1, sample2])
        self.assertEqual(1, len(result.keys()))
        self.assertNotIn('invalid_category', result)
        self.assertIn('valid_category', result)
        self.assertIn('foo', result['valid_category'])
        self.assertIn('baz', result['valid_category'])

    def test_collate_samples(self):
        """Ensure collate_samples task works."""
        sample1 = {'name': 'Sample01', KRAKEN_NAME: create_kraken(save=False)}
        sample2 = {'name': 'Sample02', KRAKEN_NAME: create_kraken(save=False)}
        samples = [sample1, sample2]
        result = collate_samples(KRAKEN_NAME, ['taxa'], samples)
        self.assertIn('Sample01', result)
        self.assertIn('Sample02', result)
        self.assertIn('taxa', result['Sample01'])
        self.assertIn('taxa', result['Sample02'])
