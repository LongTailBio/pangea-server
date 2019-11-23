"""User model definitions."""

# pylint: disable=too-many-arguments,too-few-public-methods

import datetime

from flask import current_app
from sqlalchemy import UniqueConstraint, func
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.dialects.postgresql import UUID, ENUM

from app.extensions import db, bcrypt
from app.db_models import SampleGroup


class Organization(db.Model):
    """Represent an orgnization.

    One to Many relationship to SampleGroups
    Many to Many relationship with Users
    Many to One realtionship with a User as a primary admin
    """

    __tablename__ = 'organizations'

    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    name = db.Column(db.String(128), nullable=False, unique=True)
    primary_admin_uuid = db.Column(db.ForeignKey('users.uuid'), nullable=False)
    users = association_proxy("memberships", "users")
    sample_groups = db.relationship('SampleGroup', backref='organization', lazy=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(
            self, primary_admin_uuid, name,
            is_deleted=False,
            created_at=datetime.datetime.utcnow()):
        """Initialize Pangea User model."""
        self.primary_admin_uuid = primary_admin_uuid
        self.name = name
        self.is_deleted = is_deleted
        self.created_at = created_at

    def serializable(self):
        pass

    def serialize(self):
        pass

    def add_user(self, user, role_in_org='read'):
        OrganizationMembership(
            self.uuid, user.uuid, role=role_in_org
        ).save()
        return self

    def admin_uuids(self):
        return [
            membership.user_uuid for membership in self.memberships
            if membership.role == 'admin'
        ]

    def writer_uuids(self):
        return [
            membership.user_uuid for membership in self.memberships
            if membership.role in ['admin', 'write']
        ]

    def sample_groups(self, name, description='', is_library=False, is_public=True):
        """Return a SampleGroup bound to this organization.

        Create and save the SampleGroup if it does not already exist.
        """
        sample_groups = [sg for sg in self.sample_groups if sg.name == name]
        if sample_groups:
            sample_group = sample_groups[0]
        else:
            sample_group = SampleGroup(
                name, self.uuid,
                description=description,
                is_library=is_library,
                is_public=is_public
            ).save()
        return sample_group

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def from_user(cls, user, name):
        org = cls(user.uuid, name).save()
        org.add_user(user, role_in_org='admin')
        return org.save()


class User(db.Model):
    """Pangea User model.

    To make ownership of sample libraries easier, users and organizations
    are treated as the same entity.
    """

    __tablename__ = 'users'

    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    organizations = association_proxy("memberships", "organizations")
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_fake = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    __table_args__ = (
        db.Index('_user_lower_username_idx', func.lower(username), unique=True),
    )

    def __init__(
            self, username, email,
            is_deleted=False, is_fake=False,
            created_at=datetime.datetime.utcnow()):
        """Initialize Pangea User model."""
        self.username = username
        self.email = email
        self.is_deleted = is_deleted
        self.is_fake = is_fake
        self.created_at = created_at

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class OrganizationMembership(db.Model):
    __tablename__ = 'organization_memberships'
    __table_args__ = (
        UniqueConstraint("organization_uuid", "user_uuid"),
    )
    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    organization_uuid = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('organizations.uuid'),
        index=True,
        nullable=False
    )
    user_uuid = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('users.uuid'),
        index=True,
        nullable=False
    )
    role = db.Column(
        'user_role',
        ENUM('admin', 'write', 'read', name='user_role'),
        nullable=False
    )
    organizations = db.relationship("Organization", backref="memberships", lazy=True)
    users = db.relationship("User", backref="memberships", lazy=True)

    def __init__(self, org_uuid, user_uuid, role='read'):
        self.organization_uuid = org_uuid
        self.user_uuid = user_uuid
        self.role = role

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


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
