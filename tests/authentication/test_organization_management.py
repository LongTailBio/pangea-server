"""Test suite for Organization management."""

from sqlalchemy.exc import IntegrityError
from app.authentication import Organization

from ..base import BaseTestCase
from ..utils import add_user


class TestOrganizationManagement(BaseTestCase):
    """Test suite for Organization management."""

    def test_add_user_to_organization(self):
        """Ensure user can be added to organization."""
        user = add_user('justatest', 'test@test.com', 'test')
        org = Organization.from_user(user, 'Test Organization')
        print(org.memberships)
        self.assertIn(user, org.users)

    def test_add_duplicate_users_to_organization(self):     # pylint: disable=invalid-name
        """Ensure user can only be added to organization once."""
        user = add_user('justatest', 'test@test.com', 'test')
        org = Organization.from_user(user, 'Test Organization')
        self.assertRaises(IntegrityError, lambda: org.add_user(user))

    def test_add_admin_user_to_organization(self):      # pylint: disable=invalid-name
        """Ensure user can be added to organization."""
        user1 = add_user('just test1', 'test1@test.com', 'test1')
        org = Organization.from_user(user1, 'Test Organization')
        user2 = add_user('just test2', 'test2@test.com', 'test2')
        org.add_user(user2, role_in_org='admin')
        self.assertIn(user2.uuid, [el.uuid for el in org.users])
