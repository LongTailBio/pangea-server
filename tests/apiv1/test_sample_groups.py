"""Test suite for Sample Group module."""

import json
from unittest import mock
from uuid import UUID, uuid4

from sqlalchemy.orm.exc import NoResultFound

from app import db
from app.authentication import Organization
from app.db_models import Sample, SampleGroup

from ..base import BaseTestCase
from ..utils import add_sample, add_sample_group, with_user, add_user


class TestSampleGroupModule(BaseTestCase):
    """Tests for the SampleGroup module."""

    @with_user
    def test_add_sample_group(self, auth_headers, login_user):
        """Ensure a new sample group can be added to the database."""
        org = Organization.from_user(login_user, 'Test Org')
        group_name = 'The Most Sampled of Groups'
        with self.client:
            response = self.client.post(
                '/api/v1/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=group_name,
                    organization_name=org.name,
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

    def create_group_for_organization(self, auth_headers, organization_name):
        """Create sample group for organization."""
        group_name = 'The Most Sampled of Groups'
        with self.client:
            response = self.client.post(
                '/api/v1/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=group_name,
                    organization_name=organization_name,
                )),
                content_type='application/json',
            )
            return response

    @with_user
    def test_unauthorized_add_group_with_organization(self, auth_headers, login_user):  # pylint: disable=invalid-name
        """
        Ensure a new sample group cannot be added to an organization to the user is not part of.
        """
        user = add_user('theowner', f'theowner@test.com', 'test')
        organization = Organization.from_user(user, 'My Test Org')
        response = self.create_group_for_organization(auth_headers, organization.name)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', data['status'])
        self.assertEqual('You do not have permission to write to that organization.', data['message'])

    def delete_sample_group(self, auth_headers, sample_group_id):
        """Perform request to delete sample group."""
        with self.client:
            response = self.client.delete(
                f'/api/v1/sample_groups/{str(sample_group_id)}',
                headers=auth_headers,
                content_type='application/json',
            )
            return response

    @with_user
    def _test_delete_sample_group(self, auth_headers, login_user):
        """Ensure an unowned sample group can be removed from the database."""
        sample_group = add_sample_group(name='The Least Sampled of Groups', owner=login_user)
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
    def _test_delete_owned_sample_group(self, auth_headers, login_user):
        """Ensure an owned sample group can be removed from the database by an authorized user."""
        organization = add_organization('Organization', 'admin@organization.org')
        add_member(login_user, organization, 'admin', commit=False)
        sample_group = add_sample_group(name='Owned Sample Group', owner=organization)
        db.session.commit()
        response = self.delete_sample_group(auth_headers, sample_group.uuid)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])

        # Ensure Sample Group was removed
        query = SampleGroup.query.filter_by(uuid=sample_group.uuid)
        self.assertRaises(NoResultFound, query.one)

    @with_user
    def _test_unauthorized_delete_sample_group(self, auth_headers, *_):  # pylint: disable=invalid-name
        """Ensure an owned sample group cannot be removed by an unauthorized user."""
        organization = add_organization('Organization', 'admin@organization.org')
        sample_group = add_sample_group(name='Owned Sample Group', owner=organization)
        db.session.commit()
        response = self.delete_sample_group(auth_headers, sample_group.uuid)
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', data['status'])

        # Ensure Sample Group still exists
        group = SampleGroup.query.filter_by(uuid=sample_group.uuid).one()
        self.assertTrue(group)

    @with_user
    def test_add_samples_to_group(self, auth_headers, login_user):
        """Ensure samples can be added to a sample group."""
        org = Organization.from_user(login_user, 'My Org 123ABCD')
        library = SampleGroup(name='mylibrary123123', organization_uuid=org.uuid, is_library=True).save()
        sample = library.sample('SMPL_01')
        sample_group = SampleGroup(name='mygrp123123', organization_uuid=org.uuid).save()
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
            self.assertIn(sample.uuid, [samp.uuid for samp in sample_group.samples])

    @with_user
    def test_add_duplicate_sample_group(self, auth_headers, login_user):
        """Ensure failure for non-unique Sample Group name."""
        org = Organization.from_user(login_user, 'My Org 123ABGFhCD')
        grp = SampleGroup(name='mylibrary334123', organization_uuid=org.uuid).save()
        with self.client:
            response = self.client.post(
                '/api/v1/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=grp.name,
                    organization_name=org.name,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertEqual('Duplicate group name.', data['message'])

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
            self.assertTrue('created_at' in data['data']['sample_group'])
            self.assertIn('success', data['status'])

    def test_get_single_sample_group_samples(self):  # pylint: disable=invalid-name
        """Ensure get samples for sample group behaves correctly."""
        group = add_sample_group(name='Sample Group One')
        sample00 = group.sample('SMPL_00')
        sample01 = group.sample('SMPL_01')

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

    def _test_get_group_uuid_from_name(self):
        """Ensure get sample uuid behaves correctly."""
        user = add_user('new_user RRR', 'new_user_RRR@test.com', 'somepassword')
        organization = Organization.from_user(user, 'Test Org RRR')
        sample_group_name = 'Sample Group One RRR'
        group = add_sample_group(name=sample_group_name, org=organization)
        sample_group_uuid = str(group.uuid)
        sample00 = group.sample('SMPL_00 RRR')
        sample01 = group.sample('SMPL_01 RRR')
        group.samples = [sample00, sample01]

        with self.client:
            response = self.client.get(
                (f'/api/v1/sample_groups?name={sample_group_name}'
                 f'&owner_name={organization.name}'),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(sample_group_uuid, data['data']['sample_group']['uuid'])
            self.assertEqual(sample_group_name, data['data']['sample_group']['name'])
