"""Test suite for Sample model."""

from sqlalchemy.exc import IntegrityError

from app.db_models import Sample
from tests.base import BaseTestCase

from ..utils import add_sample_group


class TestSampleModel(BaseTestCase):
    """Test suite for Sample model."""

    def test_add_sample(self):
        """Ensure sample model is created correctly."""
        library = add_sample_group('LBRY_01 AFFFS', is_library=True)
        sample = Sample(
            'SMPL_01 AFFFS',
            library.uuid,
            metadata={'subject_group': 1}
        ).save()

        self.assertTrue(sample.uuid)
        self.assertEqual(sample.name, 'SMPL_01 AFFFS')
        self.assertEqual(sample.sample_metadata['subject_group'], 1)
        self.assertEqual(sample.sample_metadata['name'], 'SMPL_01 AFFFS')
        self.assertTrue(sample.created_at)

    def test_add_duplicate_name(self):
        """Ensure duplicate sample names are not allowed."""
        library = add_sample_group('LBRY_01 OIUO', is_library=True)
        Sample(name='SMPL_01 OIUO', library_uuid=library.uuid).save()
        duplicate = Sample(name='SMPL_01 OIUO', library_uuid=library.uuid)
        self.assertRaises(IntegrityError, duplicate.save)

    def test_different_libraries(self):
        """Ensure duplicate sample names in different libraries are allowed."""
        library1 = add_sample_group('LBRY_01 UIY', is_library=True)
        library2 = add_sample_group('LBRY_02 UIY', is_library=True)
        original = Sample(name='SMPL_01 UIY', library_uuid=library1.uuid).save()
        duplicate = Sample(name='SMPL_01 UIY', library_uuid=library2.uuid).save()
        self.assertEqual(original.name, duplicate.name)
        self.assertNotEqual(original.library_uuid, duplicate.library_uuid)
