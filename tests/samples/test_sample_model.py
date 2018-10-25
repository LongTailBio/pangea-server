"""Test suite for Sample model."""

from mongoengine.errors import NotUniqueError

from app.samples.sample_models import Sample
from tests.base import BaseTestCase


class TestSampleModel(BaseTestCase):
    """Test suite for Sample model."""

    def test_add_sample(self):
        """Ensure sample model is created correctly."""
        sample = Sample(name='SMPL_01', metadata={'subject_group': 1}).save()
        # Check for runtime ID alias
        self.assertTrue(sample.id)  # pylint: disable=no-member

        self.assertTrue(sample.uuid)
        self.assertEqual(sample.name, 'SMPL_01')
        self.assertEqual(sample.metadata, {'subject_group': 1})
        self.assertTrue(sample.created_at)

    def test_add_duplicate_name(self):
        """Ensure duplicate sample names are not allowed."""
        Sample(name='SMPL_01').save()
        duplicate = Sample(name='SMPL_01')
        self.assertRaises(NotUniqueError, duplicate.save)
