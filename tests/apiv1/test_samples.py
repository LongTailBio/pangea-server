"""Test suite for Sample module."""

import json
from unittest import mock
from uuid import UUID, uuid4

from app import db
from app.samples.sample_models import Sample

from ..base import BaseTestCase
from ..utils import add_sample, add_sample_group, with_user

from .utils import middleware_tester, get_analysis_result_with_data


class TestSampleModule(BaseTestCase):
    """Tests for the Sample module."""

    @with_user
    def test_add_sample(self, auth_headers, *_):
        """Ensure a new sample can be added to the database."""
        sample_name = 'Exciting Research Starts Here'
        library = add_sample_group(name='A Great Name')
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
                    name='Exciting Research Starts Here',
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertEqual('Sample Group does not exist!', data['message'])

    def test_get_single_sample(self):
        """Ensure get single sample behaves correctly."""
        sample = add_sample(name='SMPL_01')
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/{sample_uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            sample = data['data']['sample']
            self.assertIn('SMPL_01', sample['name'])
            self.assertIn('analysis_result_uuid', sample)
            self.assertIn('created_at', sample)

    @with_user
    def test_get_all_samples(self, auth_headers, *_):
        """Test method for getting all available samples."""
        sample_names = [f'SMPL_0{i}' for i in range(10)]
        samples = [add_sample(sample_name) for sample_name in sample_names]
        with self.client:
            response = self.client.get(
                '/api/v1/samples',
                headers=auth_headers,
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']), len(samples))
            for sample in data['data']:
                self.assertIn('analysis_result_uuid', sample)
                self.assertIn('created_at', sample)

    def test_get_single_sample_metadata(self):
        """Ensure get metadata for a single sample behaves correctly."""
        metadata = {'foo': 'bar'}
        sample = add_sample(name='SMPL_01', metadata=metadata)
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/{sample_uuid}/metadata',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            sample = data['data']['sample']
            self.assertIn('uuid', sample)
            self.assertIn('name', sample)
            self.assertEqual(sample['metadata'], metadata)

    def test_get_sample_uuid_from_name(self):
        """Ensure get sample uuid behaves correctly."""
        sample_name = 'SMPL_01'
        sample = add_sample(name=sample_name)
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/samples/getid/{sample_name}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(sample_uuid, data['data']['sample_uuid'])
            self.assertEqual(sample_name, data['data']['sample_name'])

    def prepare_middleware_test(self):  # pylint: disable=no-self-use
        """Prepare database forsample  middleware test."""
        args = {
            'name': 'AncestrySample',
            'library_uuid': uuid4(),
            'metadata': {'foobar': 'baz'},
            'analysis_result': get_analysis_result_with_data(),
        }
        sample = Sample(**args).save()
        db.session.commit()

        return sample

    @with_user
    def test_kick_off_all_middleware(self, auth_headers, *_):  # pylint: disable=invalid-name
        """Ensure all middleware can be kicked off for sample."""
        sample = self.prepare_middleware_test()

        patch_path = 'app.api.v1.samples.TaskConductor.shake_that_baton'
        with mock.patch(patch_path) as conductor:
            endpoint = f'/api/v1/samples/{str(sample.uuid)}/middleware'
            middleware_tester(self, auth_headers, conductor, endpoint)
