"""Test suite for Organization module."""

import datetime
import json
import time

from uuid import uuid4

from app import db
from app.authentication.models import User, Organization
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
                    name='Test Org UYBHJGHE'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('organization', data['data'])
            self.assertIn(str(login_user.uuid), data['data']['organization']['users'])

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
        user = add_user('new_user EHYTUE', 'new_user_EHYTUE@test.com', 'somepassword')
        organization = Organization.from_user(user, 'Test Org EHYTUE')
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{organization.uuid}',
                content_type='application/json',
            )
            print(response)
            print(response.data.decode())
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Test Org EHYTUE', data['data']['organization']['name'])
            self.assertEqual(str(user.uuid), data['data']['organization']['primary_admin_uuid'])
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
        user = add_user('new_user DUYRTYD', 'new_user_DUYRTYD@test.com', 'somepassword')
        organization = Organization.from_user(user, 'Test Org DUYRTYD')
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations?name={organization.name}',
                content_type='application/json',
            )
            print(response)
            print(response.data.decode())
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(str(organization.uuid), data['data']['organization']['uuid'])

    def test_single_organization_users(self):
        """Ensure getting users for an organization behaves correctly."""
        user = add_user('new_user RQNUIAN', 'new_user_RQNUIAN@test.com', 'somepassword')
        organization = Organization.from_user(user, 'Test Org RQNUIAN')
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{organization.uuid}/users',
                content_type='application/json',
            )
            print(response)
            print(response.data.decode())
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(data['data']['users']) == 1)
            self.assertIn('success', data['status'])

    def test_single_organization_sample_groups(self):
        """Ensure getting sample groups for an organization behaves correctly."""
        user = add_user('new_user WEDFVBN', 'new_user_WEDFVBN@test.com', 'somepassword')
        org = Organization.from_user(user, 'Test Org WEDFVBN')
        group = SampleGroup(name=f'SampleGroup WEDFVBN', organization_uuid=org.uuid).save()
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations/{org.uuid}/sample_groups',
                content_type='application/json',
            )
            print(response)
            print(response.data.decode())
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['sample_groups']), 1)
            self.assertEqual(
                data['data']['sample_groups'][0]['sample_group']['name'],
                group.name
            )

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
        user = add_user('new_user ESOGH', 'new_user_ESOGH@test.com', 'somepassword')
        org1 = Organization.from_user(user, 'Test Org 1 ESOGH')
        org2 = Organization.from_user(user, 'Test Org 2 ESOGH')
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations',
                content_type='application/json',
            )
            print(response)
            print(response.data.decode())
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['organizations']), 2)

    @with_user
    def test_authorized_private_organization(self, auth_headers, login_user):
        """Ensure private organizatons show up in authorized user's list."""
        user = add_user('new_user BRBBB', 'new_user_BRBBB@test.com', 'somepassword')
        org1 = Organization.from_user(user, 'Test Public Org BRBBB', is_public=True)
        org2 = Organization.from_user(user, 'Test Private Org BRBBB', is_public=False)
        with self.client:
            response = self.client.get(
                f'/api/v1/organizations',
                content_type='application/json',
                headers=auth_headers,
            )
            print(response)
            print(response.data.decode())
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['organizations']), 2)

    @with_user
    def test_add_user_to_organization(self, auth_headers, login_user):
        """Ensure user can be added to organization by admin user."""
        organization = Organization.from_user(login_user, 'Test Org RWBMN')
        user = add_user('new_user YUT', 'new_userIUYYU@test.com', 'somepassword')
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
        user = add_user('new_user IOU', 'new_userIOU@test.com', 'somepassword')
        organization = Organization.from_user(user, 'Test Org UYHGJ')
        with self.client:
            org_uuid = str(organization.uuid)
            response = self.client.post(
                f'/api/v1/organizations/{org_uuid}/users',
                data=json.dumps(dict(
                    user_uuid=str(uuid4()),
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
        user = add_user('new_user YUYUT', 'new_userYUYUT@test.com', 'somepassword')
        organization = Organization.from_user(user, 'Test Org QQQMN')
        other_user = add_user('new_user TYDIY', 'new_userTYDIY@test.com', 'somepassword')
        with self.client:
            response = self.client.post(
                f'/api/v1/organizations/{organization.uuid}/users',
                headers=auth_headers,
                data=json.dumps(dict(
                    user_uuid=str(other_user.uuid),
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('error', data['status'])
            self.assertIn('You do not have permission to add a user to that organization.',
                          data['message'])
