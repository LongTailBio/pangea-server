"""Test suite for Reads Classified tool result model."""

from app.samples.sample_models import Sample
from app.tool_results.reads_classified import ReadsClassifiedToolResult
from app.tool_results.reads_classified.tests.constants import TEST_READS

from tests.base import BaseTestCase


class TestReadsClassifiedModel(BaseTestCase):
    """Test suite for Reads Classified tool result model."""

    def test_add_reads_classified_result(self):  # pylint: disable=invalid-name
        """Ensure Reads Classified result model is created correctly."""
        reads_classified = ReadsClassifiedToolResult(**TEST_READS)
        sample = Sample(name='SMPL_01', reads_classified=reads_classified).save()
        self.assertTrue(sample.reads_classified)
        tool_result = sample.reads_classified
        self.assertEqual(len(tool_result), 9)
        self.assertEqual(tool_result['viral'], 100)
        self.assertEqual(tool_result['archaeal'], 200)
        self.assertEqual(tool_result['bacterial'], 600)
        self.assertEqual(tool_result['nonhost_macrobial'], 0)
        self.assertEqual(tool_result['host'], 50)
        self.assertEqual(tool_result['fungal'], 0)
        self.assertEqual(tool_result['nonfungal_eukaryotic'], 0)
        self.assertEqual(tool_result['unknown'], 50)
        self.assertEqual(tool_result['total'], 0)  # 'total' is not part of fixture of data

    def test_add_partial_sites_result(self):  # pylint: disable=invalid-name
        """Ensure Reads Classified result model defaults to 0 for missing fields."""
        partial_reads = dict(TEST_READS)
        partial_reads.pop('host', None)
        partial_reads['unknown'] = 100
        reads_classified = ReadsClassifiedToolResult(**partial_reads)
        sample = Sample(name='SMPL_01', reads_classified=reads_classified).save()
        self.assertTrue(sample.reads_classified)
        tool_result = sample.reads_classified
        self.assertEqual(len(tool_result), 9)
        self.assertEqual(tool_result['viral'], 100)
        self.assertEqual(tool_result['archaeal'], 200)
        self.assertEqual(tool_result['bacterial'], 600)
        self.assertEqual(tool_result['nonhost_macrobial'], 0)
        self.assertEqual(tool_result['host'], 0)
        self.assertEqual(tool_result['fungal'], 0)
        self.assertEqual(tool_result['nonfungal_eukaryotic'], 0)
        self.assertEqual(tool_result['unknown'], 100)
        self.assertEqual(tool_result['total'], 0)  # 'total' is not part of fixture of data
