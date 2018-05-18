"""Test suite for Organization module."""

import datetime
import json
import time

from uuid import uuid4

from app import db
from app.organizations.organization_models import Organization

from tests.base import BaseTestCase
from tests.utils import add_user, add_organization, add_sample_group, with_user


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
                    name='MetaGenScope',
                    admin_email='admin@metagenscope.com'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('organization', data['data'])

            organization_uuid = data['data']['organization']['uuid']
            organization = Organization.query.filter_by(id=organization_uuid).first()
            self.assertIn(login_user, organization.admin_users)

    @with_user
    def test_add_private_organization(self, auth_headers, *_):
        """Ensure a new organization can be added to the database."""
        organization_name = 'MetaGenScope'
        with self.client:
            response = self.client.post(
                '/api/v1/organizations',
                headers=auth_headers,
                data=json.dumps(dict(
                    name=organization_name,
                    admin_email='admin@metagenscope.com',
                    access_scheme='private',
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('organization', data['data'])

        organization = Organization.query.filter_by(name=organization_name).one()
        self.assertEqual(organization.access_scheme, 'private')

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
                data=json.dumps(dict(admin_email='admin@metagenscope.com')),
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
        uuid = str(organization.id)
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{uuid}',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Organization', data['data']['organization']['name'])
            self.assertIn('admin@test.org', data['data']['organization']['admin_email'])
            self.assertTrue('created_at' in data['data']['organization'])
            self.assertTrue('users' in data['data']['organization'])
            self.assertTrue('sample_groups' in data['data']['organization'])
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

    def test_single_organization_users(self):
        """Ensure getting users for an organization behaves correctly."""
        user = add_user('test', 'test@test.com', 'test')
        organization = add_organization('Test Organization', 'admin@test.org')
        organization.users = [user]
        db.session.commit()

        uuid = str(organization.id)
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
        sample_group = add_sample_group('Pilot Sample Group')
        organization = add_organization('Test Organization', 'admin@test.org')
        organization.sample_groups = [sample_group]
        db.session.commit()

        uuid = str(organization.id)
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{uuid}/sample_groups',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data['data']['sample_groups']) == 1)
            self.assertTrue('name' in data['data']['sample_groups'][0])
            self.assertIn('success', data['status'])

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
        add_organization('Test Organization Two', 'admin@test.org')
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['organizations']), 2)
            self.assertIn('Test Organization', data['data']['organizations'][0]['name'])
            self.assertIn(
                'admin@test.org', data['data']['organizations'][0]['admin_email'])
            self.assertIn('Test Organization Two', data['data']['organizations'][1]['name'])
            self.assertIn(
                'admin@test.org', data['data']['organizations'][1]['admin_email'])
            self.assertTrue('created_at' in data['data']['organizations'][0])
            self.assertTrue('created_at' in data['data']['organizations'][1])
            self.assertIn('success', data['status'])

    def test_private_organization(self):
        """Ensure private organizatons do not show up in public list."""
        add_organization('Public Organization', 'admin@public.org')
        add_organization('Private Organization', 'admin@private.org', access_scheme='private')
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations',
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['organizations']), 1)
            self.assertIn('Public Organization', data['data']['organizations'][0]['name'])

    @with_user
    def test_authorized_private_organization(self, auth_headers, login_user):
        """Ensure private organizatons show up in authorized user's list."""
        add_organization('Public Organization', 'admin@public.org',
                         created_at=datetime.datetime.utcnow())
        time.sleep(0.3)
        private_org = add_organization('Private Organization', 'admin@private.org',
                                       access_scheme='private',
                                       created_at=datetime.datetime.utcnow())
        private_org.users.append(login_user)
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
            self.assertIn('Public Organization', data['data']['organizations'][0]['name'])
            self.assertIn('Private Organization', data['data']['organizations'][1]['name'])

    @with_user
    def test_add_user_to_organiztion(self, auth_headers, login_user):
        """Ensure user can be added to organization by admin user."""
        organization = add_organization('Test Organization', 'admin@test.org')
        organization.add_admin(login_user)
        db.session.commit()
        user = add_user('new_user', 'new_user@test.com', 'somepassword')
        with self.client:
            org_uuid = str(organization.id)
            response = self.client.post(
                f'/api/v1/organizations/{org_uuid}/users',
                headers=auth_headers,
                data=json.dumps(dict(
                    user_id=str(user.id),
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
            org_uuid = str(organization.id)
            response = self.client.post(
                f'/api/v1/organizations/{org_uuid}/users',
                data=json.dumps(dict(
                    user_id=user_uuid,
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
            org_uuid = str(organization.id)
            response = self.client.post(
                f'/api/v1/organizations/{org_uuid}/users',
                headers=auth_headers,
                data=json.dumps(dict(
                    user_id=user_uuid,
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('You do not have permission to add a user to that group.',
                          data['message'])
            self.assertIn('error', data['status'])

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
        sample_group = add_sample_group('The Most Sampled of Groups')
        organization = add_organization('Test Organization', 'admin@test.org')
        organization.users.append(login_user)
        db.session.commit()

        response = self.add_group_to_organization(auth_headers,
                                                  sample_group.id,
                                                  organization.id)

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertIn(sample_group, organization.sample_groups)

    @with_user
    def test_unauthorized_add_group_to_organiztion(self, auth_headers, *_):
        """Ensure sample group can be added to organization by member."""
        sample_group = add_sample_group('The Most Sampled of Groups')
        organization = add_organization('Test Organization', 'admin@test.org')

        response = self.add_group_to_organization(auth_headers,
                                                  sample_group.id,
                                                  organization.id)

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('error', data['status'])
