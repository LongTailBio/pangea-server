"""Organization model definitions."""

import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import fields

from app.base import BaseSchema
from app.extensions import db
from app.users.user_models import UserSchema
from app.sample_groups.sample_group_models import SampleGroupSchema


# pylint: disable=too-few-public-methods
class OrganizationMembership(db.Model):
    """Association object for linking users to organizations with role."""

    __tablename__ = 'users_organizations'
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), primary_key=True)
    organization_id = db.Column(UUID(as_uuid=True),
                                db.ForeignKey('organizations.id'),
                                primary_key=True)

    role = db.Column(db.String(128), default='member', nullable=False)

    # Bidirectional attribute/collection of "organization"/"organization_users"
    organization = db.relationship('Organization', backref='organization_users')

    # Bidirectional attribute/collection of "user"/"user_organizations"
    user = db.relationship('User', backref='user_organizations')

    def __init__(self, user=None, organization=None, role='member'):
        """Initialize Organization/User association object."""
        self.organization = organization
        self.user = user
        self.role = role


# pylint: disable=too-few-public-methods
class Organization(db.Model):
    """MetaGenScope Organization model."""

    __tablename__ = 'organizations'

    # pylint: disable=invalid-name
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text('uuid_generate_v4()'))
    name = db.Column(db.String(128), unique=True, nullable=False)
    admin_email = db.Column(db.String(128), nullable=False)
    access_scheme = db.Column(db.String(128), default='public', nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    # Use association proxy to skip association object for most cases
    users = association_proxy('organization_users', 'user')

    admin_memberships = db.relationship(
        'OrganizationMembership',
        primaryjoin='and_(Organization.id==OrganizationMembership.organization_id, '
                    'OrganizationMembership.role==\'admin\')',
        viewonly=True)
    admin_users = association_proxy('admin_memberships', 'user')

    sample_groups = db.relationship(
        'SampleGroup',
        backref='organization',
        lazy='dynamic')

    def __init__(self, name, admin_email, access_scheme='public',
                 created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope Organization model."""
        self.name = name
        self.admin_email = admin_email
        self.access_scheme = access_scheme
        self.created_at = created_at

    def add_admin(self, admin_user):
        """Add admin user to organization."""
        membership = OrganizationMembership.query.filter_by(organization=self,
                                                            user=admin_user).first()
        if not membership:
            membership = OrganizationMembership(organization=self, user=admin_user)
            db.session.add(membership)
        membership.role = 'admin'
        db.session.commit()


class OrganizationSchema(BaseSchema):
    """Serializer for Organization model."""

    __envelope__ = {
        'single': 'organization',
        'many': 'organizations',
    }
    __model__ = Organization

    uuid = fields.Str()
    name = fields.Str()
    admin_email = fields.Str()
    users = fields.Nested(UserSchema, many=True)
    sample_groups = fields.Nested(SampleGroupSchema, many=True)
    created_at = fields.Date()


organization_schema = OrganizationSchema()   # pylint: disable=invalid-name
