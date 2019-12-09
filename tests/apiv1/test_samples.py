"""Test suite for Sample module."""

import json
from unittest import mock
from uuid import UUID, uuid4

from app import db
from app.db_models import Sample

from ..base import BaseTestCase
from ..utils import (
    add_sample,
    add_sample_group,
    with_user,
)

from .utils import middleware_tester, get_analysis_result_with_data


class TestSampleModule(BaseTestCase):
    """Tests for the Sample module."""

    @with_user
    def test_add_sample(self, auth_headers, *_):
        """Ensure a new sample can be added to the database."""
        sample_name = 'Exciting Research Starts Here KJDHHDF'
        library = add_sample_group(is_library=True)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=sample_name,
                    library_uuid=str(library.uuid),
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('uuid', data['data']['sample'])
            self.assertEqual(sample_name, data['data']['sample']['name'])

        sample_uuid = UUID(data['data']['sample']['uuid'])
        self.assertIn(sample_uuid, library.sample_uuids)

    @with_user
    def test_add_sample_missing_group(self, auth_headers, *_):
        """Ensure adding a sample with an invalid group uuid fails."""
        sample_group_uuid = str(uuid4())
        with self.client:
            response = self.client.post(
                f'/api/v1/samples',
                headers=auth_headers,
                data=json.dumps(dict(
                    library_uuid=sample_group_uuid,
                    name='Exciting Research Starts Here KCJLKD',
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertEqual('Library does not exist!', data['message'])

    def test_get_single_sample(self):
        """Ensure get single sample behaves correctly."""
        library = add_sample_group(is_library=True)
        sample = library.sample('SMPL_01 HHHGJGH')
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/{sample.uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            sample = data['data']['sample']
            self.assertIn('SMPL_01', sample['name'])
            self.assertIn('analysis_result_uuids', sample)
            self.assertIn('created_at', sample)

    @with_user
    def test_get_all_samples(self, auth_headers, login_user):
        """Test method for getting all available samples."""
        library = add_sample_group('my_library EURWILT', owner=login_user, is_library=True)
        samples = [library.sample(f'SMPL_0{i} UUOUY') for i in range(10)]
        with self.client:
            response = self.client.get(
                '/api/v1/samples',
                headers=auth_headers,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['samples']), len(samples))

    def test_get_single_sample_metadata(self):
        """Ensure get metadata for a single sample behaves correctly."""
        metadata = {'foo': 'bar'}
        library = add_sample_group(is_library=True)
        sample = library.sample('SMPL_01 HHHGJGH', metadata=metadata)
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/{sample.uuid}/metadata',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            sample = data['data']['sample']
            self.assertIn('uuid', sample)
            self.assertIn('name', sample)
            self.assertEqual(sample['metadata'], metadata)
