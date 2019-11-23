"""Test suite for Organization module."""

import datetime
import json
import time

from uuid import uuid4

from app import db
from app.authentication.models import User
from app.db_models import SampleGroup

from ..base import BaseTestCase
from ..utils import add_user, add_sample_group, with_user


class TestOrganizationModule(BaseTestCase):
    """Tests for the Organizations module."""

    @with_user
    def test_add_organization(self, auth_headers, login_user):
        """Ensure a new organization can be added to the database."""
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=auth_headers,
                data=json.dumps(dict(
                    username='MetaGenScope',
                    email='admin@metagenscope.com',
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('organization', data['data'])

            organization_uuid = data['data']['organization']['uuid']
            admin_users = User.query.filter(
                User.organization_memberships.any(organization_uuid=organization_uuid,
                                                  role='admin'),
            ).all()
            self.assertIn(login_user, admin_users)

    # pylint: disable=invalid-name
    @with_user
    def test_add_organization_invalid_json(self, auth_headers, *_):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=auth_headers,
                data=json.dumps(dict()),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid organization payload.', data['message'])
            self.assertIn('error', data['status'])

    # pylint: disable=invalid-name
    @with_user
    def test_add_organization_invalid_json_keys(self, auth_headers, *_):
        """Ensure error is thrown if the JSON object does not have a name key."""
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=auth_headers,
                data=json.dumps(dict(email='admin@metagenscope.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid organization payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_invalid_token(self):
        """Ensure create organization route fails for invalid token."""
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=dict(Authorization='Bearer invalid'))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_single_organization(self):
        """Ensure get single organization behaves correctly."""
        organization = add_organization('Test Organization', 'admin@test.org')
        uuid = str(organization.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Organization', data['data']['organization']['username'])
            self.assertIn('admin@test.org', data['data']['organization']['email'])
            self.assertTrue('created_at' in data['data']['organization'])
            self.assertIn('success', data['status'])

    def test_single_organization_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/blah',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('error', data['status'])
            self.assertIn('Invalid organization UUID.', data['message'])

    def test_get_uuid_from_name(self):
        """Ensure get organization UUID behaves correctly."""
        organization_name = 'Sample Group One'
        organization = add_organization(name=organization_name, email='admin@test.org')
        organization_uuid = str(organization.uuid)

        with self.client:
            response = self.client.get(
                f'/api/v1/organizations?name={organization_name}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(organization_uuid, data['data']['organization']['uuid'])
            self.assertEqual(organization_name, data['data']['organization']['username'])

    def test_single_organization_users(self):
        """Ensure getting users for an organization behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        organization = add_organization('Test Organization', 'admin@test.org')
        add_member(user, organization, 'read')
        db.session.commit()

        uuid = str(organization.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{uuid}/users',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data['data']['users']) == 1)
            self.assertTrue('username' in data['data']['users'][0])
            self.assertTrue('email' in data['data']['users'][0])
            self.assertIn('success', data['status'])

    def test_single_organization_sample_groups(self):
        """Ensure getting sample groups for an organization behaves correctly."""
        organization = add_organization('Test Organization', 'admin@test.org')
        sample_group = add_sample_group('Pilot Sample Group', owner=organization)
        db.session.commit()

        uuid = str(organization.uuid)
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{uuid}/sample_groups',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['sample_groups']), 1)
            self.assertEqual(data['data']['sample_groups'][0]['name'], sample_group.name)

    def test_single_organization_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        random_uuid = str(uuid4())
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{random_uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Organization does not exist', data['message'])
            self.assertIn('error', data['status'])

    def test_all_organizations(self):
        """Ensure get all organizations behaves correctly."""
        add_organization('Test Organization', 'admin@test.org')
        add_organization('Test Organization Two', 'admin@example.org')
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['organizations']), 2)
            self.assertIn('Test Organization', data['data']['organizations'][0]['username'])
            self.assertIn(
                'admin@test.org', data['data']['organizations'][0]['email'])
            self.assertIn('Test Organization Two', data['data']['organizations'][1]['username'])
            self.assertIn(
                'admin@example.org', data['data']['organizations'][1]['email'])
            self.assertTrue('created_at' in data['data']['organizations'][0])
            self.assertTrue('created_at' in data['data']['organizations'][1])
            self.assertIn('success', data['status'])

    @with_user
    def test_authorized_private_organization(self, auth_headers, login_user):
        """Ensure private organizatons show up in authorized user's list."""
        add_organization('Public Organization', 'admin@public.org',
                         created_at=datetime.datetime.utcnow())
        time.sleep(0.3)
        private_org = add_organization('Private Organization', 'admin@private.org',
                                       created_at=datetime.datetime.utcnow())
        add_member(login_user, private_org, 'admin', commit=False)
        db.session.commit()
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations',
                content_type='application/json',
                headers=auth_headers,
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['organizations']), 2)
            self.assertIn('Public Organization', data['data']['organizations'][0]['username'])
            self.assertIn('Private Organization', data['data']['organizations'][1]['username'])

    @with_user
    def test_add_user_to_organiztion(self, auth_headers, login_user):
        """Ensure user can be added to organization by admin user."""
        organization = add_organization('Test Organization', 'admin@test.org')
        add_member(login_user, organization, 'admin', commit=False)
        db.session.commit()
        user = add_user('new_user', 'new_user@test.com', 'somepassword')
        with self.client:
            org_uuid = str(organization.uuid)
            response = self.client.post(
                f'/api/v1/organizations/{org_uuid}/users',
                headers=auth_headers,
                data=json.dumps(dict(
                    user_uuid=str(user.uuid),
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(user, organization.users)
            self.assertIn('success', data['status'])

    def test_unauthenticated_add_user_to_organiztion(self):
        """Ensure unauthenticated user cannot attempt action."""
        organization = add_organization('Test Organization', 'admin@test.org')
        user_uuid = str(uuid4())
        with self.client:
            org_uuid = str(organization.uuid)
            response = self.client.post(
                f'/api/v1/organizations/{org_uuid}/users',
                data=json.dumps(dict(
                    user_uuid=user_uuid,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertIn('Provide a valid auth token.', data['message'])
            self.assertIn('error', data['status'])

    @with_user
    def test_unauthorized_add_user_to_organiztion(self, auth_headers, *_):
        """Ensure user cannot be added to organization by non-organization admin user."""
        organization = add_organization('Test Organization', 'admin@test.org')
        user_uuid = str(uuid4())
        with self.client:
            org_uuid = str(organization.uuid)
            response = self.client.post(
                f'/api/v1/organizations/{org_uuid}/users',
                headers=auth_headers,
                data=json.dumps(dict(
                    user_uuid=user_uuid,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('error', data['status'])
            self.assertIn('You do not have permission to add a user to that organization.',
                          data['message'])

    def add_group_to_organization(self, auth_headers, group_uuid, organization_uuid):
        """Add sample group to organization."""
        with self.client:
            response = self.client.post(
                f'/api/v1/organizations/{str(organization_uuid)}/sample_groups',
                headers=auth_headers,
                data=json.dumps(dict(
                    sample_group_uuid=str(group_uuid),
                )),
                content_type='application/json',
            )
            return response

    @with_user
    def test_add_group_to_organiztion(self, auth_headers, login_user):
        """Ensure sample group can be added to organization by member."""
        sample_group = add_sample_group('The Most Sampled of Groups', owner=login_user)
        organization = add_organization('Test Organization', 'admin@test.org')
        add_member(login_user, organization, 'admin', commit=False)
        db.session.commit()

        response = self.add_group_to_organization(auth_headers,
                                                  sample_group.uuid,
                                                  organization.uuid)

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        # Refresh DB model
        sample_group = SampleGroup.filter_by(uuid=sample_group.uuid).one()
        self.assertEqual(sample_group.owner_name, organization.username)
        self.assertEqual(sample_group.owner_uuid, organization.uuid)

    @with_user
    def test_unauthorized_add_group_to_organiztion(self, auth_headers, *_):
        """Ensure sample group can be added to organization by member."""
        sample_group = add_sample_group('The Most Sampled of Groups')
        organization = add_organization('Test Organization', 'admin@test.org')

        response = self.add_group_to_organization(auth_headers,
                                                  sample_group.uuid,
                                                  organization.uuid)

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', data['status'])
