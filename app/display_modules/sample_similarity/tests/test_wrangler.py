"""Test suite for Sample Similarity Wrangler."""

from app import db
from app.display_modules.sample_similarity.wrangler import SampleSimilarityWrangler
from app.samples.sample_models import Sample
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.kraken.tests.factory import create_kraken
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.krakenhll.tests.factory import create_krakenhll
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.metaphlan2.tests.factory import create_metaphlan2

from tests.base import BaseTestCase
from tests.utils import add_sample_group


KRAKEN_NAME = KrakenResultModule.name()
KRAKENHLL_NAME = KrakenHLLResultModule.name()
METAPHLAN2_NAME = Metaphlan2ResultModule.name()


class TestSampleSimilarityWrangler(BaseTestCase):
    """Test suite for Sample Similarity Wrangler."""

    def test_run_sample_group(self):
        """Ensure run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            metadata = {'foobar': f'baz{i}'}
            sample_data = {
                'name': f'Sample{i}',
                'metadata': metadata,
                KRAKEN_NAME: create_kraken(),
                KRAKENHLL_NAME: create_krakenhll(),
                METAPHLAN2_NAME: create_metaphlan2(),
            }
            return Sample(**sample_data).save()

        sample_group = add_sample_group(name='SampleGroup01')
        samples = [create_sample(i) for i in range(6)]
        sample_group.samples = samples
        db.session.commit()
        SampleSimilarityWrangler.help_run_sample_group(sample_group,
                                                       samples,
                                                       'sample_similarity').get()
        analysis_result = sample_group.analysis_result
        self.assertIn('sample_similarity', analysis_result)
        sample_similarity = analysis_result.sample_similarity
        self.assertEqual(sample_similarity.status, 'S')
