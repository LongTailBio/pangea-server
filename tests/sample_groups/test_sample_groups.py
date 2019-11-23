"""Test suite for Sample Group model."""

from uuid import uuid4

from sqlalchemy.exc import IntegrityError

from app import db
from app.db_models import Sample, SampleGroup

from ..base import BaseTestCase
from ..utils import add_sample_group


class TestSampleGroupModel(BaseTestCase):
    """Test suite for SampleGroup model."""

    def test_add_sample_group(self):
        """Ensure sample group model is created correctly."""
        group = add_sample_group('Sample Group One')
        self.assertTrue(group.uuid)
        self.assertEqual(group.name, 'Sample Group One')
        self.assertTrue(group.created_at)

    def test_add_user_duplicate_name(self):
        """Ensure duplicate group names are not allowed."""
        add_sample_group('Sample Group One')
        self.assertRaises(IntegrityError, lambda: add_sample_group('Sample Group One'))

    def test_add_samples(self):
        """Ensure that samples can be added to SampleGroup."""
        sample_group = add_sample_group('Sample Group One')
        sample_one = Sample(name='SMPL_01',
                            library_uuid=uuid4(),
                            metadata={'subject_group': 1})
        sample_two = Sample(name='SMPL_02',
                            library_uuid=uuid4(),
                            metadata={'subject_group': 4})
        sample_group.samples = [sample_one, sample_two]
        db.session.commit()

        samples = sample_group.samples
        sample_uuids = [sample.uuid for sample in samples]
        self.assertEqual(len(samples), 2)
        self.assertIn(sample_one.uuid, sample_uuids)
        self.assertIn(sample_two.uuid, sample_uuids)
        self.assertEqual(len(samples), 2)
        self.assertIn(sample_one, samples)
        self.assertIn(sample_two, samples)
