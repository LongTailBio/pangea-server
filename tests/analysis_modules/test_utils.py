"""Test suite for Conductor tasks."""

from app.analysis_modules.utils import fetch_samples
from app.extensions import db

from ..base import BaseTestCase
from ..utils import add_sample, add_sample_group


class TestConductorTasks(BaseTestCase):
    """Test suite for Conductor tasks."""

    def test_fetch_samples(self):
        """Ensure fetch_samples tasks works as expected."""
        group = add_sample_group('Sample Group One', access_scheme='public')
        group.samples = [add_sample(f'Sample {i}') for i in range(5)]
        db.session.commit()

        samples = fetch_samples(group.id)
        self.assertEqual(len(samples), 5)
