"""Test suite for Average Genome Size Wrangler."""

from app import db
from app.display_modules.ags import AGSDisplayModule
from app.display_modules.ags.ags_wrangler import AGSWrangler
from app.samples.sample_models import Sample
from app.tool_results.microbe_census.tests.factory import create_microbe_census

from tests.base import BaseTestCase
from tests.utils import add_sample_group


class TestAverageGenomeSizeWrangler(BaseTestCase):
    """Test suite for Average Genome Size Wrangler."""

    def test_run_sample_group(self):
        """Ensure run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            metadata = {'foobar': f'baz{i}'}
            return Sample(name=f'Sample{i}',
                          metadata=metadata,
                          microbe_census=create_microbe_census()).save()

        sample_group = add_sample_group(name='SampleGroup01')
        samples = [create_sample(i) for i in range(10)]
        sample_group.samples = samples
        db.session.commit()
        AGSWrangler.help_run_sample_group(sample_group, samples, AGSDisplayModule).get()
        analysis_result = sample_group.analysis_result
        self.assertIn('average_genome_size', analysis_result)
        average_genome_size = analysis_result.average_genome_size.fetch()
        self.assertEqual(average_genome_size.status, 'S')
