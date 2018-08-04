"""Test suite for Sample Similarity result type."""

import json
from uuid import uuid4

from tests.base import BaseTestCase
from tests.factories.analysis_result import AnalysisResultMetaFactory


class TestSampleSimilarityModule(BaseTestCase):
    """Tests for the Sample Similarity module."""

    def test_get_sample_similarity(self):
        """Ensure getting a single sample similarity behaves correctly."""
        analysis_result = AnalysisResultMetaFactory(processed=True)
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{analysis_result.id}/sample_similarity',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(data['data']['status'], 'S')
            self.assertIn('data', data['data'])
            sample_similarity = data['data']['data']
            self.assertIn('categories', sample_similarity)
            self.assertIn('tools', sample_similarity)
            self.assertIn('data_records', sample_similarity)
            self.assertTrue(len(sample_similarity['data_records']) > 0)
            self.assertIn('SampleID', sample_similarity['data_records'][0])

    def test_get_pending_sample_similarity(self):  # pylint: disable=invalid-name
        """Ensure getting a pending single sample similarity behaves correctly."""
        analysis_result = AnalysisResultMetaFactory()
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{analysis_result.id}/sample_similarity',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('status', data['data'])
            self.assertEqual(data['data']['status'], 'P')

    def test_get_malformed_id_sample_similarity(self):  # pylint: disable=invalid-name
        """Ensure getting a malformed ID for a single sample similarity behaves correctly."""
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/foobarblah/sample_similarity',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid UUID provided.', data['message'])
            self.assertIn('error', data['status'])

    def test_get_missing_sample_similarity(self):  # pylint: disable=invalid-name
        """Ensure getting a missing single sample similarity behaves correctly."""
        random_uuid = uuid4()

        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{random_uuid}/sample_similarity',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Analysis Result does not exist.', data['message'])
            self.assertIn('error', data['status'])
