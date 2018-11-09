"""Test suite for Organization management."""

from sqlalchemy.orm.exc import FlushError

from app import db
from app.authentication.models import User, OrganizationMembership
from ..base import BaseTestCase
from ..utils import add_user, add_organization


class TestOrganizationManagement(BaseTestCase):
    """Test suite for Organization management."""

    def test_add_user_to_organization(self):
        """Ensure user can be added to organization."""
        organization = add_organization('Test Organization', 'admin@test.org')
        user = add_user('justatest', 'test@test.com', 'test')
        organization.users.append(user)
        db.session.commit()
        self.assertIn(user, organization.users)

    def test_add_duplicate_users_to_organization(self):     # pylint: disable=invalid-name
        """Ensure user can only be added to organization once."""
        organization = add_organization('Test Organization', 'admin@test.org')
        user = add_user('justatest', 'test@test.com', 'test')
        with db.session.no_autoflush:
            organization.users.append(user)
            db.session.commit()
            organization.users.append(user)
            self.assertRaises(FlushError, db.session.commit)

    def test_set_admin_user_to_organization(self):      # pylint: disable=invalid-name
        """Ensure user can be added to organization."""
        organization = add_organization('Test Organization', 'admin@test.org')
        user = add_user('justatest', 'test@test.com', 'test')
        admin_membership = OrganizationMembership('admin')
        admin_membership.user = user
        organization.users.append(admin_membership)
        db.session.commit()
        admin_users = User.query.filter(
            User.uuid == organization.uuid,
            User.user_memberships.any(role='admin'),
        )
        self.assertIn(user, admin_users)
