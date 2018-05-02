"""Test suite for AGS result type."""

import json
from uuid import uuid4

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.ags.tests.factory import AGSFactory
from tests.base import BaseTestCase


class TestAGSModule(BaseTestCase):
    """Tests for the AGS module."""

    def test_get_ags(self):
        """Ensure getting a single AGS result works correctly."""
        average_genome_size = AGSFactory()
        wrapper = AnalysisResultWrapper(data=average_genome_size, status='S').save()
        analysis_result = AnalysisResultMeta(average_genome_size=wrapper).save()
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{analysis_result.id}/average_genome_size',
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertIn('success', data['status'])
            self.assertEqual(data['data']['status'], 'S')
            self.assertIn('data', data['data'])
            ags_result = data['data']['data']
            self.assertIn('categories', ags_result)
            self.assertIn('distributions', ags_result)
            self.assertTrue(len(ags_result['distributions']) > 0)

    def test_get_pending_average_genome_size(self):  # pylint: disable=invalid-name
        """Ensure getting a pending AGS behaves correctly."""
        average_genome_size = AGSFactory()
        wrapper = AnalysisResultWrapper(data=average_genome_size).save()
        analysis_result = AnalysisResultMeta(average_genome_size=wrapper).save()
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{analysis_result.uuid}/average_genome_size',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(data['data']['status'], 'P')

    def test_get_malformed_id_sample_similarity(self):  # pylint: disable=invalid-name
        """Ensure getting a malformed ID for a AGS behaves correctly."""
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/foobarblah/average_genome_size',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid UUID provided.', data['message'])
            self.assertIn('error', data['status'])

    def test_get_missing_average_genome_size(self):  # pylint: disable=invalid-name
        """Ensure getting a missing AGS behaves correctly."""

        random_uuid = uuid4()

        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{random_uuid}/average_genome_size',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Analysis Result does not exist.', data['message'])
            self.assertIn('error', data['status'])
