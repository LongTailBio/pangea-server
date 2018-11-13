"""Test suite for the authorization endpoints."""

# pylint: disable=invalid-name

import json
import time

from app.extensions import db
from ..base import BaseTestCase
from ..utils import add_user, with_user


class TestAuthBlueprint(BaseTestCase):
    """Test suite for the authorization endpoints."""

    def test_user_registration(self):
        """Test user registration."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='justatest',
                    email='test@test.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data']['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registration_duplicate_email(self):
        """Ensure registration fails with duplicate email address."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='michael',
                    email='test@test.com',
                    password='test'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_duplicate_username(self):
        """Ensure registration fails with duplicate email username."""
        add_user('test', 'test@test.com', 'test')
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='test',
                    email='test@test.com2',
                    password='test'
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That user already exists.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json(self):
        """Ensure registration fails for invalid JSON payload."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid registration payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        """Ensure registration fails for JSON payload missing username key."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(email='test@test.com', password='test')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid registration payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        """Ensure registration fails for JSON payload missing email key."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='justatest', password='test')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid registration payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        """Ensure registration fails for JSON payload missing password key."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/register',
                data=json.dumps(dict(
                    username='justatest', email='test@test.com')),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid registration payload.', data['message'])
            self.assertIn('error', data['status'])

    def test_registered_user_login(self):
        """Ensure login works for registered user."""
        with self.client:
            add_user('test', 'test+registered@test.com', 'test')
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test+registered@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data']['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_not_registered_user_login(self):
        """Ensure login fails without a registered user."""
        with self.client:
            response = self.client.post(
                '/api/v1/auth/login',
                data=json.dumps(dict(
                    email='test+unregistered@test.com',
                    password='test'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 404)

    @with_user
    def test_valid_logout(self, auth_headers, *_):
        """Ensure client can log out."""
        with self.client:
            # Valid token logout
            response = self.client.get(
                '/api/v1/auth/logout',
                headers=auth_headers
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)

    @with_user
    def test_invalid_logout_expired_token(self, auth_headers, *_):
        """Ensure logout fails for expired token."""
        with self.client:
            # Invalid token logout
            time.sleep(4.5)
            response = self.client.get(
                '/api/v1/auth/logout',
                headers=auth_headers
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')

    def test_invalid_logout(self):
        """Ensure logout fails for invalid token."""
        with self.client:
            response = self.client.get(
                '/api/v1/auth/logout',
                headers=dict(Authorization='Bearer invalid'))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    @with_user
    def test_user_status(self, auth_headers, *_):
        """Ensure user status route works."""
        with self.client:
            response = self.client.get(
                '/api/v1/auth/status',
                headers=auth_headers
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'success')
            self.assertTrue(data['data'] is not None)
            self.assertEqual(data['data']['user']['username'], 'test')
            self.assertEqual(data['data']['user']['email'], 'test@test.com')
            self.assertTrue(data['data']['user']['created_at'])
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        """Ensure user status route fails for invalid request."""
        with self.client:
            response = self.client.get(
                '/api/v1/auth/status',
                headers=dict(Authorization='Bearer invalid'))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(
                data['message'] == 'Invalid token. Please log in again.')
            self.assertEqual(response.status_code, 401)

    @with_user
    def test_invalid_logout_deleted(self, auth_headers, login_user):
        """Ensure logout fails for inactive user."""
        # Update user
        login_user.is_deleted = True
        db.session.commit()
        with self.client:
            response = self.client.get(
                '/api/v1/auth/logout',
                headers=auth_headers
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'User is not active')
            self.assertEqual(response.status_code, 401)

    @with_user
    def test_invalid_status_inactive(self, auth_headers, login_user):
        """Ensure user session fails for inactive user."""
        # Update user
        login_user.is_deleted = True
        db.session.commit()
        with self.client:
            response = self.client.get(
                '/api/v1/auth/status',
                headers=auth_headers
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'error')
            self.assertTrue(data['message'] == 'User is not active')
            self.assertEqual(response.status_code, 401)
