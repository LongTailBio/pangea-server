"""Test suite for Conductor tasks."""

from analysis_packages.top_taxa import TopTaxaAnalysisModule
from analysis_packages.top_taxa.tests.factory import create_values
from analysis_packages.base_data.krakenhll.constants import MODULE_NAME as KRAKENHLL_NAME

from app.analysis_modules.utils import fetch_samples, filter_samples
from app.extensions import db

from tests.base import BaseTestCase
from tests.utils import add_sample, add_sample_group


class TestConductorTasks(BaseTestCase):
    """Test suite for Conductor tasks."""

    def test_fetch_samples(self):
        """Ensure fetch_samples tasks works as expected."""
        group = add_sample_group('Sample Group One', access_scheme='public')
        group.samples = [add_sample(f'Sample {i}') for i in range(5)]
        db.session.commit()

        samples = fetch_samples(group.id)
        self.assertEqual(len(samples), 5)

    def test_filter_samples(self):
        """Ensure filter_sample removes samples without required tool results."""
        complete_values = create_values()
        sample_complete = add_sample(name='Complete Sample',
                                     metadata={'foo': f'bar'},
                                     sample_kwargs=complete_values)
        incomplete_values = create_values()
        incomplete_values.pop(KRAKENHLL_NAME, None)
        sample_incomplete = add_sample(name='Incomplete Sample',
                                       metadata={'foo': f'bar'},
                                       sample_kwargs=incomplete_values)
        samples = [sample_complete, sample_incomplete]
        module = TopTaxaAnalysisModule
        filtered_samples = filter_samples(samples, module)
        self.assertEqual(len(filtered_samples), 1)
        self.assertEqual(filtered_samples[0]['name'], 'Complete Sample')
