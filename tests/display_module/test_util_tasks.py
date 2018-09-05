"""Test suite for Display Module utility tasks."""

from tool_packages.kraken import KrakenResultModule
from tool_packages.kraken.tests.factory import create_result as create_kraken

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.sample_similarity.tests.factory import create_mvp_sample_similarity
from app.display_modules.utils import (
    categories_from_metadata,
    persist_result_helper,
    collate_samples,
)
from app.samples.sample_models import Sample

from tests.base import BaseTestCase
from tests.utils import add_sample_group


KRAKEN_NAME = KrakenResultModule.name()


class TestDisplayModuleUtilityTasks(BaseTestCase):
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
        sample1 = Sample(name='Sample01', metadata=metadata1).save()
        sample2 = Sample(name='Sample02', metadata=metadata2).save()
        result = categories_from_metadata.delay([sample1, sample2]).get()
        self.assertEqual(1, len(result.keys()))
        self.assertNotIn('invalid_category', result)
        self.assertIn('valid_category', result)
        self.assertIn('foo', result['valid_category'])
        self.assertIn('baz', result['valid_category'])

    def test_persist_result_helper(self):
        """Ensure persist_result_helper works as intended."""
        wrapper = AnalysisResultWrapper().save()
        analysis_result = AnalysisResultMeta(sample_similarity=wrapper).save()
        sample_similarity = create_mvp_sample_similarity()

        persist_result_helper(sample_similarity,
                              analysis_result.uuid,
                              'sample_similarity')
        analysis_result.reload()
        self.assertIn('sample_similarity', analysis_result)
        wrapper = getattr(analysis_result, 'sample_similarity').fetch()
        self.assertIn('status', wrapper)
        self.assertEqual('S', wrapper.status)

    def test_collate_samples(self):
        """Ensure collate_samples task works."""
        sample1_data = {'name': 'Sample01', KRAKEN_NAME: create_kraken()}
        sample2_data = {'name': 'Sample02', KRAKEN_NAME: create_kraken()}
        sample1 = Sample(**sample1_data).save()
        sample2 = Sample(**sample2_data).save()
        sample_group = add_sample_group(name='SampleGroup01')
        sample_group.samples = [sample1, sample2]
        db.session.commit()

        samples = [sample.fetch_safe() for sample in [sample1, sample2]]
        result = collate_samples.delay(KRAKEN_NAME, ['taxa'], samples).get()
        self.assertIn('Sample01', result)
        self.assertIn('Sample02', result)
        self.assertIn('taxa', result['Sample01'])
        self.assertIn('taxa', result['Sample02'])
