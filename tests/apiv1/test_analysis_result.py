"""Test suite for AnalysisResults module."""

import json

from app.db_models import Sample, SampleAnalysisResult, SampleGroupAnalysisResult
from tests.base import BaseTestCase

from ..utils import add_sample_group


class TestAnalysisResultModule(BaseTestCase):
    """Test suite for AnalysisResults module."""

    def test_get_single_sample_result(self):
        """Ensure get single analysis result behaves correctly."""
        library = add_sample_group('LBRY_01', is_library=True)
        sample = library.sample('SMPL_01')
        analysis_result = sample.analysis_result('module_1')
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{str(analysis_result.uuid)}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('uuid', data['data']['analysis_result'])
            self.assertIn('module_name', data['data']['analysis_result'])

    def test_get_single_group_result(self):
        """Ensure get single analysis result behaves correctly."""
        library = add_sample_group('LBRY_01', is_library=True)
        analysis_result = library.analysis_result('module_1')
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/{str(analysis_result.uuid)}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('uuid', data['data']['analysis_result'])
            self.assertIn('module_name', data['data']['analysis_result'])
