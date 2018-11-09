"""User model definitions."""

# pylint: disable=too-many-arguments,too-few-public-methods

import datetime

from flask import current_app
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import fields

from app.base import BaseSchema
from app.extensions import db, bcrypt


class OrganizationMembership(db.Model):
    """Association object for linking users to organizations with role."""

    __tablename__ = 'organization_memberships'

    organization_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'),
                                  primary_key=True, nullable=False)
    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'),
                          primary_key=True, nullable=False)
    role = db.Column(ENUM('admin', 'write' 'read', name='organization_role'),
                     nullable=False)
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('organization_uuid', 'user_uuid', name='_organization_user_uc'),
    )

    def __init__(
            self, role, organization_uuid=None, user_uuid=None,
            is_public=True, created_at=datetime.datetime.utcnow()):
        """Initialize organization membership model."""
        if organization_uuid:
            self.organization_uuid = organization_uuid
        if user_uuid:
            self.user_uuid = user_uuid
        self.role = role
        self.is_public = is_public
        self.created_at = created_at


class User(db.Model):
    """Pangea User model.

    To make ownership of sample libraries easier, users and organizations
    are treated as the same entity.
    """

    __tablename__ = 'users'

    uuid = db.Column(UUID(as_uuid=True),
                     primary_key=True,
                     server_default=db.text('uuid_generate_v4()'))
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    user_type = db.Column(ENUM('user', 'organization', name='user_type'),
                          nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_fake = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.Index('_user_lower_username_idx', func.lower(username), unique=True),
    )

    # Users that belong to this organization
    user_memberships = db.relationship(
        'OrganizationMembership',
        primaryjoin='User.uuid == OrganizationMembership.organization_uuid',
        backref=db.backref('organization'),
    )
    users = association_proxy('user_memberships', 'user')

    # Organizations this user belongs to
    organization_memberships = db.relationship(
        'OrganizationMembership',
        primaryjoin='User.uuid == OrganizationMembership.user_uuid',
        backref=db.backref('user'),
    )
    organizations = association_proxy('organization_memberships', 'organization')

    def __init__(
            self, username, email, user_type,
            is_deleted=False, is_fake=False,
            created_at=datetime.datetime.utcnow()):
        """Initialize Pangea User model."""
        self.username = username
        self.email = email
        self.user_type = user_type
        self.is_deleted = is_deleted
        self.is_fake = is_fake
        self.created_at = created_at


class PasswordAuthentication(db.Model):
    """Password Authentication model.

    Pangea will support multiple authentication modes, each stored separately.
    """

    __tablename__ = 'password_authentication'

    user_uuid = db.Column(UUID(as_uuid=True), db.ForeignKey('users.uuid'),
                          primary_key=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    # One-to-one relationship with User
    user = db.relationship('User', backref=db.backref('password_authentication', uselist=False))

    def __init__(
            self, password, user_uuid=None,
            created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope User model."""
        if user_uuid:
            self.user_uuid = user_uuid
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.created_at = created_at


class UserSchema(BaseSchema):
    """Serializer for User."""

    __envelope__ = {
        'single': 'user',
        'many': 'users',
    }
    __model__ = User

    uuid = fields.Str()
    username = fields.Str()
    email = fields.Str()


user_schema = UserSchema()      # pylint: disable=invalid-name
