"""Test suite for User model."""

from sqlalchemy.exc import IntegrityError

from app import db
from app.users.user_models import User
from ..base import BaseTestCase
from ..utils import add_user


class TestUserModel(BaseTestCase):
    """Test suite for User model."""

    def test_add_user(self):
        """Ensure user model is created correctly."""
        user = add_user('justatest', 'test@test.com', 'test')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'justatest')
        self.assertEqual(user.email, 'test@test.com')
        self.assertTrue(user.password)
        self.assertTrue(user.active)
        self.assertTrue(user.created_at)

    # pylint: disable=invalid-name
    def test_add_user_duplicate_username(self):
        """Ensure duplicate usernames are not allowed."""
        add_user('justatest', 'test@test.com', 'password')
        duplicate_user = User(
            username='justatest',
            email='test@test2.com',
            password='password',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        """Ensure duplicate email addresses are not allowed."""
        add_user('justatest', 'test@test.com', 'password')
        duplicate_user = User(
            username='justanothertest',
            email='test@test.com',
            password='password',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        """Ensure passwords are random."""
        user_one = add_user('justatest', 'test@test.com', 'test')
        user_two = add_user('justatest2', 'test@test2.com', 'test')
        self.assertNotEqual(user_one.password, user_two.password)

    def test_encode_auth_token(self):
        """Ensure auth token is encoded correctly."""
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        """Ensure auth token is decoded correctly."""
        user = add_user('justatest', 'test@test.com', 'test')
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token), user.id)
