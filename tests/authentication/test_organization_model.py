"""Test suite for Organization model."""

from sqlalchemy.exc import IntegrityError

from app import db
from app.authentication import User, Organization
from ..base import BaseTestCase
from ..utils import add_user


class TestOrganizationModel(BaseTestCase):
    """Test suite for Organization model."""

    def test_add_organization(self):
        """Ensure organization model is created correctly."""
        user = add_user('justatest', 'test@test.com', 'test')
        org = Organization.from_user(user, 'Test Organization')

        self.assertTrue(org.uuid)
        self.assertEqual(org.name, 'Test Organization')
        self.assertEqual(org.primary_admin_uuid, user.uuid)
        self.assertTrue(org.created_at)

    # pylint: disable=invalid-name
    def test_add_organziation_duplicate_name(self):
        """Ensure duplicate names are not allowed."""
        user = add_user('justatest', 'test@test.com', 'test')
        Organization.from_user(user, 'Test Organization')
        self.assertRaises(IntegrityError, lambda: Organization.from_user(user, 'Test Organization'))
