"""Test suite for Organization model."""

from sqlalchemy.exc import IntegrityError

from app import db
from app.organizations.organization_models import Organization
from ..base import BaseTestCase
from ..utils import add_organization


class TestOrganizationModel(BaseTestCase):
    """Test suite for Organization model."""

    def test_add_organization(self):
        """Ensure organization model is created correctly."""
        organization = add_organization('Test Organization', 'admin@test.org')
        self.assertTrue(organization.id)
        self.assertEqual(organization.name, 'Test Organization')
        self.assertEqual(organization.admin_email, 'admin@test.org')
        self.assertTrue(organization.created_at)

    # pylint: disable=invalid-name
    def test_add_organziation_duplicate_name(self):
        """Ensure duplicate names are not allowed."""
        add_organization('Test Organization', 'admin@test.org')
        duplicate_organization = Organization(
            name='Test Organization',
            admin_email='test@test2.org',
        )
        db.session.add(duplicate_organization)
        self.assertRaises(IntegrityError, db.session.commit)
