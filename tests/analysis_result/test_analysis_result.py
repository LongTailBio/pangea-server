"""Test suite for Analysis Results model."""

from sqlalchemy.exc import IntegrityError

from app.db_models import (
    Sample,
    SampleAnalysisResult,
    SampleGroupAnalysisResult,
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

    def test_add_duplicate_to_diff_samples(self):
        """Ensure duplicate sample names in different libraries are allowed."""
        library = add_sample_group('LBRY_01', is_library=True)
        s1 = Sample(name='SMPL_01', library_uuid=library.uuid).save()
        s2 = Sample(name='SMPL_02', library_uuid=library.uuid).save()
        orig = SampleAnalysisResult('module_1', s1.uuid).save()
        dup = SampleAnalysisResult('module_1', s2.uuid).save()
        self.assertEqual(orig.module_name, dup.module_name)
        self.assertNotEqual(orig.parent_uuid, dup.parent_uuid)

    def test_add_ar_to_group(self):
        """Ensure sample model is created correctly."""
        library = add_sample_group('LBRY_01', is_library=True)
        ar = SampleGroupAnalysisResult('module_1', library.uuid).save()
        self.assertTrue(ar.uuid)
        self.assertEqual(ar.module_name, 'module_1')
        self.assertEqual(ar.parent_uuid, library.uuid)
        self.assertTrue(ar.created_at)

    def test_add_duplicate_module_to_group(self):
        """Ensure duplicate sample names are not allowed."""
        grp = add_sample_group('GRP_01 UIHHGHJ')
        SampleGroupAnalysisResult('module_1 UIHHGHJ', grp.uuid).save()
        dup = SampleGroupAnalysisResult('module_1 UIHHGHJ', grp.uuid)
        self.assertRaises(IntegrityError, dup.save)

    def test_add_duplicate_to_diff_groups(self):
        """Ensure duplicate sample names in different libraries are allowed."""
        g1 = add_sample_group('GRP_01 HHJH')
        g2 = add_sample_group('GRP_02 HHJH')
        orig = SampleGroupAnalysisResult('module_1 HHJH', g1.uuid).save()
        dup = SampleGroupAnalysisResult('module_1 HHJH', g2.uuid).save()
        self.assertEqual(orig.module_name, dup.module_name)
        self.assertNotEqual(orig.parent_uuid, dup.parent_uuid)
