"""Test suite for Analysis Results model."""

from sqlalchemy.exc import IntegrityError

from app.db_models import (
    Sample,
    SampleAnalysisResult,
)
from tests.base import BaseTestCase

from ..utils import add_sample_group


class TestAnalysisResultModel(BaseTestCase):
    """Test suite for Sample model."""

    def test_add_ar_to_sample(self):
        """Ensure sample model is created correctly."""
        library = add_sample_group('LBRY_01', is_library=True)
        sample = Sample('SMPL_01', library.uuid,).save()
        ar = SampleAnalysisResult('module_1', sample.uuid).save()
        self.assertTrue(ar.uuid)
        self.assertEqual(ar.module_name, 'module_1')
        self.assertEqual(ar.parent_uuid, sample.uuid)
        self.assertTrue(ar.created_at)

    def test_add_duplicate_module_to_sample(self):
        """Ensure duplicate sample names are not allowed."""
        library = add_sample_group('LBRY_01', is_library=True)
        sample = Sample(name='SMPL_01', library_uuid=library.uuid).save()
        SampleAnalysisResult('module_1', sample.uuid).save()
        dup = SampleAnalysisResult('module_1', sample.uuid)
        self.assertRaises(IntegrityError, dup.save)

    def test_different_libraries(self):
        """Ensure duplicate sample names in different libraries are allowed."""
        library = add_sample_group('LBRY_01', is_library=True)
        s1 = Sample(name='SMPL_01', library_uuid=library.uuid).save()
        s2 = Sample(name='SMPL_02', library_uuid=library.uuid).save()
        orig = SampleAnalysisResult('module_1', s1.uuid).save()
        dup = SampleAnalysisResult('module_1', s2.uuid).save()
        self.assertEqual(orig.module_name, dup.module_name)
        self.assertNotEqual(orig.parent_uuid, dup.parent_uuid)
