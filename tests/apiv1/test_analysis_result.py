"""Test suite for AnalysisResults module."""

import json

from app.db_models import (
    Sample,
    SampleAnalysisResult,
    SampleGroupAnalysisResult,
    SampleAnalysisResultField,
    SampleGroupAnalysisResultField,
)
from tests.base import BaseTestCase

from ..utils import add_sample_group


class TestAnalysisResultModule(BaseTestCase):
    """Test suite for AnalysisResults module."""

    def test_get_sample_result_from_names(self):
        """Ensure get sample analysis result based on names works."""
        lib_name, sample_name, module_name = 'LBRY_01 UISADD', 'SMPL_01 UISADD', 'module_1 UISADD'
        library = add_sample_group(lib_name, is_library=True)
        sample = library.sample(sample_name)
        analysis_result = sample.analysis_result(module_name)
        ar_field_1 = analysis_result.field('field_1').set_data('data_1')
        ar_field_2 = analysis_result.field('field_2').set_data('data_2')
        BY_NAME_URL = f'/api/v1/analysis_results/byname/{lib_name}/{sample_name}/{module_name}'
        with self.client:
            response = self.client.get(
                BY_NAME_URL,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            print(data)
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('field_1', data['data'])
            self.assertEqual('data_1', data['data']['field_1'])
            self.assertIn('field_2', data['data'])
            self.assertEqual('data_2', data['data']['field_2'])

    def test_create_sample_result_ar_from_names(self):
        """Ensure creating an analysis result field behaves correctly."""
        lib_name, sample_name, module_name = 'LBRY_01 YTHEH', 'SMPL_01 YTHEH', 'module_1 YTHEH'
        library = add_sample_group(lib_name, is_library=True)
        sample = library.sample(sample_name)
        analysis_result = sample.analysis_result(module_name)
        BY_NAME_URL = f'/api/v1/analysis_results/byname/{lib_name}/{sample_name}/{module_name}'
        with self.client:
            response = self.client.post(
                BY_NAME_URL + f'/field_2',
                content_type='application/json',
                data=json.dumps({
                    'field_2': {
                        "value_1": 100,
                        "value_2": "Fields may either be s3 uris or simple JSON blobs"
                    }
                }),
            )
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data.decode())
            uuid = data['data']['analysis_result_field']['uuid']
            field = SampleAnalysisResultField.query.filter_by(uuid=uuid).first()
            self.assertEqual(field.field_name, 'field_2')
            self.assertEqual(field.parent_uuid, analysis_result.uuid)

    def test_get_s3uri_sample_result_ar_from_names(self):
        """Ensure get single analysis result behaves correctly."""
        lib_name, sample_name = 'LBRY_01 HRAVWQ', 'SMPL_01 HRAVWQ'
        module_name, field_name = 'module_1 HRAVWQ', 'field_1 HRAVWQ'
        library = add_sample_group(lib_name, is_library=True)
        sample = library.sample(sample_name)
        analysis_result = sample.analysis_result(module_name)
        BY_NAME_URL = f'/api/v1/analysis_results/byname/{lib_name}/{sample_name}/{module_name}'
        with self.client:
            response = self.client.get(
                BY_NAME_URL + f'/{field_name}/s3uri?ext=foo',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('endpoint_url', data['data'])
            self.assertIn('__type__', data['data'])
            self.assertIn('uri', data['data'])

    def test_get_group_result_from_names(self):
        """Ensure get group analysis result based on names works."""
        lib_name, module_name = 'LBRY_01 RRRR', 'module_1 RRRR'
        library = add_sample_group(lib_name, is_library=True)
        analysis_result = library.analysis_result(module_name)
        ar_field_1 = analysis_result.field('field_1').set_data('data_1')
        ar_field_2 = analysis_result.field('field_2').set_data('data_2')
        BY_NAME_URL = f'/api/v1/analysis_results/byname/group/{lib_name}/{module_name}'
        with self.client:
            response = self.client.get(
                BY_NAME_URL,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('field_1', data['data'])
            self.assertEqual('data_1', data['data']['field_1'])
            self.assertIn('field_2', data['data'])
            self.assertEqual('data_2', data['data']['field_2'])

    def test_create_group_result_ar_from_names(self):
        """Ensure creating an analysis result field behaves correctly."""
        lib_name, module_name = 'LBRY_01 FQAA', 'module_1 FQAA'
        library = add_sample_group(lib_name, is_library=True)
        analysis_result = library.analysis_result(module_name)
        BY_NAME_URL = f'/api/v1/analysis_results/byname/group/{lib_name}/{module_name}'
        with self.client:
            response = self.client.post(
                BY_NAME_URL + f'/field_2',
                content_type='application/json',
                data=json.dumps({
                    'field_2': {
                        "value_1": 100,
                        "value_2": "Fields may either be s3 uris or simple JSON blobs"
                    }
                }),
            )
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data.decode())
            uuid = data['data']['analysis_result_field']['uuid']
            field = SampleGroupAnalysisResultField.query.filter_by(uuid=uuid).first()
            self.assertEqual(field.field_name, 'field_2')
            self.assertEqual(field.parent_uuid, analysis_result.uuid)

    def test_get_s3uri_group_result_ar_from_names(self):
        """Ensure get single analysis result behaves correctly."""
        lib_name, module_name, field_name = 'LBRY_01 POIU', 'module_1 POIU', 'field_1 POIU'
        library = add_sample_group(lib_name, is_library=True)
        analysis_result = library.analysis_result(module_name)
        BY_NAME_URL = f'/api/v1/analysis_results/byname/group/{lib_name}/{module_name}'
        with self.client:
            response = self.client.get(
                BY_NAME_URL + f'/{field_name}/s3uri?ext=foo',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('endpoint_url', data['data'])
            self.assertIn('__type__', data['data'])
            self.assertIn('uri', data['data'])

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
