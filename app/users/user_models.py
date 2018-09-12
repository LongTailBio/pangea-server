"""User model definitions."""

import datetime
import uuid
import jwt

from flask import current_app
from flask_api.exceptions import AuthenticationFailed
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.associationproxy import association_proxy
from marshmallow import fields

from app.base import BaseSchema
from app.extensions import db, bcrypt


class User(db.Model):
    """MetaGenScope User model."""

    __tablename__ = 'users'

    # pylint: disable=invalid-name
    id = db.Column(UUID(as_uuid=True),
                   primary_key=True,
                   server_default=db.text('uuid_generate_v4()'))
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    # Use association proxy to skip association object for most cases
    organizations = association_proxy('user_organizations', 'organization')

    def __init__(
            self, username, email, password,
            created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope User model."""
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.created_at = created_at

    @classmethod
    def encode_auth_token(cls, user_id):
        """Generate the auth token."""
        try:
            days = current_app.config.get('TOKEN_EXPIRATION_DAYS')
            seconds = current_app.config.get('TOKEN_EXPIRATION_SECONDS')
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=days, seconds=seconds),
                'iat': datetime.datetime.utcnow(),
                'sub': str(user_id)
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS512',
            )
        except Exception as e:  # pylint: disable=broad-except
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decode the auth token - :param auth_token: - :return: UUID|string."""
        try:
            secret = current_app.config.get('SECRET_KEY')
            payload = jwt.decode(auth_token, secret, algorithms=['HS512'])
            return uuid.UUID(payload['sub'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Signature expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token. Please log in again.')


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
