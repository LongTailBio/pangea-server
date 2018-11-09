"""Test suite for Sample Group module."""

import json
from unittest import mock
from uuid import UUID, uuid4

from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup

from ..base import BaseTestCase
from ..utils import add_sample, add_sample_group, with_user, add_organization

from .utils import middleware_tester, get_analysis_result_with_data


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
            sample_group = SampleGroup.query.filter_by(uuid=sample_group_id).one()
            self.assertTrue(sample_group.analysis_result)

    def create_group_for_organization(self, auth_headers, organization_uuid):
        """Create sample group for organization."""
        group_name = 'The Most Sampled of Groups'
        with self.client:
            response = self.client.post(
                '/api/v1/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=group_name,
                    organization_uuid=str(organization_uuid),
                )),
                content_type='application/json',
            )
            return response

    @with_user
    def test_add_group_with_organization(self, auth_headers, login_user):  # pylint: disable=invalid-name
        """Ensure a new sample group can be added with an organization."""
        organization = add_organization('Organization', 'admin@organization.org')
        organization.users.append(login_user)
        db.session.commit()
        response = self.create_group_for_organization(auth_headers, organization.uuid)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        sample_group_uuid = UUID(data['data']['sample_group']['uuid'])

        organization_groups = organization.sample_groups
        sample_group_uuids = [group.uuid for group in organization_groups]
        self.assertIn(sample_group_uuid, sample_group_uuids)

    @with_user
    def test_unauthorized_add_group_with_organization(self, auth_headers, *_):  # pylint: disable=invalid-name
        """
        Ensure a new sample group cannot be added to an organization to the user is not part of.
        """
        organization = add_organization('Organization', 'admin@organization.org')
        response = self.create_group_for_organization(auth_headers, organization.uuid)
        self.assertEqual(response.status_code, 403)

    def delete_sample_group(self, auth_headers, sample_group_id):
        """Perform request to delete sample group."""
        with self.client:
            response = self.client.delete(
                f'/api/v1/sample_groups/{sample_group_id}',
                headers=auth_headers,
                content_type='application/json',
            )
            return response

    @with_user
    def test_delete_sample_group(self, auth_headers, *_):
        """Ensure an unowned sample group can be removed from the database."""
        sample_group = add_sample_group(name='The Least Sampled of Groups')
        sample = add_sample(name='SMPL_01')
        sample_group.samples = [sample]
        db.session.commit()
        response = self.delete_sample_group(auth_headers, sample_group.uuid)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])

        # Ensure Sample Group was removed
        query = SampleGroup.query.filter_by(uuid=sample_group.uuid)
        self.assertRaises(NoResultFound, query.one)

    @with_user
    def test_delete_owned_sample_group(self, auth_headers, login_user):
        """Ensure an owned sample group can be removed from the database by an authorized user."""
        organization = add_organization('Organization', 'admin@organization.org')
        organization.users.append(login_user)
        sample_group = add_sample_group(name='Owned Sample Group')
        organization.sample_groups.append(sample_group)
        db.session.commit()
        response = self.delete_sample_group(auth_headers, sample_group.uuid)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])

        # Ensure Sample Group was removed
        query = SampleGroup.query.filter_by(uuid=sample_group.uuid)
        self.assertRaises(NoResultFound, query.one)

    @with_user
    def test_unauthorized_delete_sample_group(self, auth_headers, *_):  # pylint: disable=invalid-name
        """Ensure an owned sample group cannot be removed by an unauthorized user."""
        organization = add_organization('Organization', 'admin@organization.org')
        sample_group = add_sample_group(name='Owned Sample Group')
        organization.sample_groups.append(sample_group)
        db.session.commit()
        response = self.delete_sample_group(auth_headers, sample_group.uuid)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', data['status'])

        # Ensure Sample Group still exists
        group = SampleGroup.query.filter_by(uuid=sample_group.uuid).one()
        self.assertTrue(group)

    @with_user
    def test_add_samples_to_group(self, auth_headers, *_):
        """Ensure samples can be added to a sample group."""
        sample_group = add_sample_group(name='A Great Name')
        sample = add_sample(name='SMPL_01')
        endpoint = f'/api/v1/sample_groups/{str(sample_group.uuid)}/samples'
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
            self.assertIn(sample.uuid, sample_group.sample_uuids)

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
        group_uuid = str(group.uuid)
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
                f'/api/v1/sample_groups/{str(group.uuid)}/samples',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertIn('samples', data['data'])
            self.assertEqual(len(data['data']['samples']), 2)
            self.assertTrue(any(s['name'] == 'SMPL_00' for s in data['data']['samples']))
            self.assertTrue(any(s['name'] == 'SMPL_01' for s in data['data']['samples']))

    def test_get_group_uuid_from_name(self):
        """Ensure get sample uuid behaves correctly."""
        sample_group_name = 'Sample Group One'
        group = add_sample_group(name=sample_group_name)
        sample_group_uuid = str(group.uuid)
        sample00 = add_sample(name='SMPL_00')
        sample01 = add_sample(name='SMPL_01')
        group.samples = [sample00, sample01]
        db.session.commit()

        with self.client:
            response = self.client.get(
                f'/api/v1/sample_groups/getid/{sample_group_name}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(sample_group_uuid, data['data']['sample_group_uuid'])
            self.assertEqual(sample_group_name, data['data']['sample_group_name'])

    def prepare_middleware_test(self):  # pylint: disable=no-self-use
        """Prepare database for middleware test."""
        def create_sample(i):
            """Create unique sample for index i."""
            args = {
                'library_uuid': uuid4(),
                'analysis_result': get_analysis_result_with_data(),
                'name': f'AncestrySample{i}',
                'metadata': {'foobar': f'baz{i}'},
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

        patch_path = 'app.api.v1.samples.TaskConductor.shake_that_baton'
        with mock.patch(patch_path) as conductor:
            endpoint = f'/api/v1/sample_groups/{str(sample_group.uuid)}/middleware'
            middleware_tester(self, auth_headers, conductor, endpoint)
