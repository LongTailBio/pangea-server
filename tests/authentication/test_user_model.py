"""Test suite for User model."""

from sqlalchemy.exc import IntegrityError

from app import db
from app.authentication.helpers import encode_auth_token, decode_auth_token
from app.authentication import User
from ..base import BaseTestCase
from ..utils import add_user


class TestUserModel(BaseTestCase):
    """Test suite for User model."""

    def test_add_user(self):
        """Ensure user model is created correctly."""
        user = add_user('justatest', 'test@test.com', 'test')
        self.assertTrue(user.uuid)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password_authentication)
        self.assertFalse(user.is_deleted)
        self.assertTrue(user.created_at)

    # pylint: disable=invalid-name
    def test_add_user_duplicate_username(self):
        """Ensure duplicate usernames are not allowed."""
        add_user('justatest', 'test@test.com', 'password')
        duplicate_user = User(
            username='justatest',
            email='test@test2.com',
        )
        self.assertRaises(IntegrityError, duplicate_user.save)

    def test_add_user_duplicate_email(self):
        """Ensure duplicate email addresses are not allowed."""
        add_user('justatest', 'test@test.com', 'password')
        duplicate_user = User(
            username='justanothertest',
            email='test@test.com',
        )
        self.assertRaises(IntegrityError, duplicate_user.save)

    def test_passwords_are_random(self):
        """Ensure passwords are random."""
        user_one = add_user('justatest', 'test@test.com', 'test')
        user_two = add_user('justatest2', 'test@test2.com', 'test')
        self.assertNotEqual(
            user_one.password_authentication.password,
            user_two.password_authentication.password
        )

    def test_encode_auth_token(self):
        """Ensure auth token is encoded correctly."""
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = encode_auth_token(user)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        """Ensure auth token is decoded correctly."""
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = encode_auth_token(user)
        self.assertTrue(isinstance(auth_token, bytes))
        authn = decode_auth_token(auth_token)
        self.assertEqual(authn.sub, user.uuid)
