"""Test suite for Sample model."""

from uuid import uuid4

from mongoengine.errors import NotUniqueError
from app.samples.sample_models import Sample
from tests.base import BaseTestCase


class TestSampleModel(BaseTestCase):
    """Test suite for Sample model."""

    def test_add_sample(self):
        """Ensure sample model is created correctly."""
        sample = Sample(name='SMPL_01',
                        library_uuid=uuid4(),
                        metadata={'subject_group': 1}).save()
        # Check for runtime ID alias
        self.assertTrue(sample.id)  # pylint: disable=no-member

        self.assertTrue(sample.uuid)
        self.assertEqual(sample.name, 'SMPL_01')
        self.assertEqual(sample.metadata, {'subject_group': 1})
        self.assertTrue(sample.created_at)

    def test_add_duplicate_name(self):
        """Ensure duplicate sample names are not allowed."""
        library_uuid = uuid4()
        Sample(name='SMPL_01', library_uuid=library_uuid).save()
        duplicate = Sample(name='SMPL_01', library_uuid=library_uuid)
        self.assertRaises(NotUniqueError, duplicate.save)

    def test_different_libraries(self):
        """Ensure duplicate sample names in different libraries are allowed."""
        original = Sample(name='SMPL_01', library_uuid=uuid4()).save()
        duplicate = Sample(name='SMPL_01', library_uuid=uuid4()).save()
        self.assertEqual(original.name, duplicate.name)
        self.assertNotEqual(original.library_uuid, duplicate.library_uuid)
