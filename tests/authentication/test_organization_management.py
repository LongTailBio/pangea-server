"""Test suite for Organization management."""

from sqlalchemy.exc import IntegrityError

from app import db
from app.authentication.models import User
from ..base import BaseTestCase
from ..utils import add_user, add_organization, add_member


class TestOrganizationManagement(BaseTestCase):
    """Test suite for Organization management."""

    def test_add_user_to_organization(self):
        """Ensure user can be added to organization."""
        organization = add_organization('Test Organization', 'admin@test.org')
        user = add_user('justatest', 'test@test.com', 'test')
        add_member(user, organization, 'read', commit=False)
        db.session.commit()
        self.assertIn(user, organization.users)

    def test_add_duplicate_users_to_organization(self):     # pylint: disable=invalid-name
        """Ensure user can only be added to organization once."""
        organization = add_organization('Test Organization', 'admin@test.org')
        user = add_user('justatest', 'test@test.com', 'test')
        add_member(user, organization, 'read', commit=False)
        db.session.commit()
        add_member(user, organization, 'read', commit=False)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_admin_user_to_organization(self):      # pylint: disable=invalid-name
        """Ensure user can be added to organization."""
        organization = add_organization('Test Organization', 'admin@test.org')
        user = add_user('justatest', 'test@test.com', 'test')
        add_member(user, organization, 'admin', commit=False)
        db.session.commit()
        admin_users = User.query.filter(
            User.organization_memberships.any(organization_uuid=organization.uuid,
                                              role='admin'),
        ).all()
        self.assertIn(user, admin_users)
