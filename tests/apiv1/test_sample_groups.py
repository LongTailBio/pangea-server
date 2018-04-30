"""Test suite for Sample Group module."""

import json

from app import db
from app.display_modules.ancestry.constants import TOOL_MODULE_NAME
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.ancestry.tests.factory import create_ancestry

from tests.base import BaseTestCase
from tests.utils import add_sample, add_sample_group, with_user


class TestSampleGroupModule(BaseTestCase):
    """Tests for the SampleGroup module."""

    @with_user
    def test_add_sample_group(self, auth_headers, *_):
        """Ensure a new sample group can be added to the database."""
        group_name = 'The Most Sampled of Groups'
        with self.client:
            response = self.client.post(
                '/api/v1/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=group_name,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertEqual(group_name, data['data']['sample_group']['name'])

            # Ensure Analysis Result was created
            sample_group_id = data['data']['sample_group']['uuid']
            sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
            self.assertTrue(sample_group.analysis_result)

    @with_user
    def test_add_samples_to_group(self, auth_headers, *_):
        """Ensure samples can be added to a sample group."""
        sample_group = add_sample_group(name='A Great Name')
        sample = add_sample(name='SMPL_01')
        endpoint = f'/api/v1/sample_groups/{str(sample_group.id)}/samples'
        with self.client:
            response = self.client.post(
                endpoint,
                headers=auth_headers,
                data=json.dumps(dict(
                    sample_uuids=[str(sample.uuid)],
                )),
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode())
            self.assertIn('success', data['status'])
            self.assertIn(sample.uuid, sample_group.sample_ids)

    @with_user
    def test_add_duplicate_sample_group(self, auth_headers, *_):
        """Ensure failure for non-unique Sample Group name."""
        group_name = 'The Most Sampled of Groups'
        add_sample_group(name=group_name)
        with self.client:
            response = self.client.post(
                '/api/v1/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=group_name,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertEqual('Sample Group with that name already exists.', data['message'])

    def test_get_single_sample_groups(self):
        """Ensure get single group behaves correctly."""
        group = add_sample_group(name='Sample Group One')
        group_uuid = str(group.id)
        with self.client:
            response = self.client.get(
                f'/api/v1/sample_groups/{group_uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Sample Group One', data['data']['sample_group']['name'])
            self.assertIn('public', data['data']['sample_group']['access_scheme'])
            self.assertTrue('created_at' in data['data']['sample_group'])
            self.assertIn('success', data['status'])

    def test_get_single_sample_group_samples(self):  # pylint: disable=invalid-name
        """Ensure get samples for sample group behaves correctly."""
        group = add_sample_group(name='Sample Group One')
        sample00 = add_sample(name='SMPL_00')
        sample01 = add_sample(name='SMPL_01')
        group.samples = [sample00, sample01]
        db.session.commit()

        with self.client:
            response = self.client.get(
                f'/api/v1/sample_groups/{str(group.id)}/samples',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('samples', data['data'])
            self.assertEqual(len(data['data']['samples']), 2)
            self.assertTrue(any(s['name'] == 'SMPL_00' for s in data['data']['samples']))
            self.assertTrue(any(s['name'] == 'SMPL_01' for s in data['data']['samples']))

    def prepare_middleware_test(self):  # pylint: disable=no-self-use
        """Prepare database for middleware test."""
        def create_sample(i):
            """Create unique sample for index i."""
            data = create_ancestry()
            args = {
                'name': f'AncestrySample{i}',
                'metadata': {'foobar': f'baz{i}'},
                TOOL_MODULE_NAME: data,
            }
            return Sample(**args).save()

        sample_group = add_sample_group(name='Ancestry Sample Group')
        sample_group.samples = [create_sample(i) for i in range(6)]
        db.session.commit()

        return sample_group

    @with_user
    def test_kick_off_all_middleware(self, auth_headers, *_):  # pylint: disable=invalid-name
        """Ensure all middleware can be kicked off for group."""
        sample_group = self.prepare_middleware_test()

        with self.client:
            response = self.client.post(
                f'/api/v1/sample_groups/{str(sample_group.id)}/middleware',
                headers=auth_headers,
                content_type='application/json',
            )
            self.assertEqual(response.status_code, 202)
            data = json.loads(response.data.decode())
            self.assertEqual(data['data']['message'], 'Started middleware')
