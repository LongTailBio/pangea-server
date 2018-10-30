"""Test suite for Conductor tasks."""

from analysis_packages.top_taxa import TopTaxaAnalysisModule
from analysis_packages.top_taxa.tests.factory import create_values
from analysis_packages.krakenhll_data.constants import MODULE_NAME as KRAKENHLL_NAME

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
