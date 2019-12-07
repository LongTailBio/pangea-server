"""Test suite for AnalysisResults module."""

import json

from app.db_models import Sample, SampleAnalysisResult, SampleGroupAnalysisResult
from tests.base import BaseTestCase

from ..utils import add_sample_group


class TestAnalysisResultModule(BaseTestCase):
    """Test suite for AnalysisResults module."""

    def test_get_sample_result_from_names(self):
        """Ensure get single analysis result behaves correctly."""
        assert False
        lib_name, sample_name, module_name = 'LBRY_01 YTHEH', 'SMPL_01 YTHEH', 'module_1 YTHEH'
        library = add_sample_group(lib_nameb, is_library=True)
        sample = library.sample(sample_name)
        analysis_result = sample.analysis_result(module_name)
        with self.client:
            response = self.client.get(
                f'/api/v1/analysis_results/byname/{lib_name}/{sample_name}/{module_name}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('uuid', data['data']['analysis_result'])
            self.assertIn('module_name', data['data']['analysis_result'])

    def test_create_sample_result_ar_from_names(self):
        """Ensure get single analysis result behaves correctly."""
        assert False
        lib_name, sample_name, module_name = 'LBRY_01 YTHEH', 'SMPL_01 YTHEH', 'module_1 YTHEH'
        library = add_sample_group(lib_nameb, is_library=True)
        sample = library.sample(sample_name)
        analysis_result = sample.analysis_result(module_name)
        with self.client:
            response = self.client.post(
                f'/api/v1/analysis_results/byname/{lib_name}/{sample_name}/{module_name}/{field_name}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('uuid', data['data']['analysis_result'])
            self.assertIn('module_name', data['data']['analysis_result'])

    def test_spec_uri_sample_result_ar_from_names(self):
        """Ensure get single analysis result behaves correctly."""
        assert False
        lib_name, sample_name, module_name = 'LBRY_01 YTHEH', 'SMPL_01 YTHEH', 'module_1 YTHEH'
        library = add_sample_group(lib_nameb, is_library=True)
        sample = library.sample(sample_name)
        analysis_result = sample.analysis_result(module_name)
        with self.client:
            response = self.client.post(
                f'/api/v1/analysis_results/byname/{lib_name}/{sample_name}/{module_name}/{field_name}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('uuid', data['data']['analysis_result'])
            self.assertIn('module_name', data['data']['analysis_result'])

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
