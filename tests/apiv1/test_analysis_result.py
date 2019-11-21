"""Test suite for AnalysisResults module."""

import json

from app.db_models import SampleAnalysisResult
from tests.base import BaseTestCase


class TestAnalysisResultModule(BaseTestCase):
    """Test suite for AnalysisResults module."""

    def test_get_single_result(self):
        """Ensure get single analysis result behaves correctly."""
        analysis_result = AnalysisResult().save()
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{str(analysis_result.uuid)}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('analysis_result', data['data'])
            self.assertIn('uuid', data['data']['analysis_result'])
            self.assertIn('result_types', data['data']['analysis_result'])
            self.assertIn('created_at', data['data']['analysis_result'])
