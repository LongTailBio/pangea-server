"""Helper methods related to User model."""

from functools import wraps

import datetime
import uuid
import jwt

from flask import request, current_app
from flask_api.exceptions import NotAuthenticated, AuthenticationFailed

from app.authentication.models import User


# TODO: encode role for each group membership
def encode_auth_token(user_uuid):
    """Generate the auth token."""
    try:
        days = current_app.config.get('TOKEN_EXPIRATION_DAYS')
        seconds = current_app.config.get('TOKEN_EXPIRATION_SECONDS')
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(
                days=days, seconds=seconds),
            'iat': datetime.datetime.utcnow(),
            'sub': str(user_uuid)
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS512',
        )
    except Exception as exc:  # pylint: disable=broad-except
        return exc


# Decode to "AuthManager" type allowing easier interogation of memberships
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


# TODO: Return AuthManager object rather than UUID
def authenticate(required=True):
    """Decorate API route calls requiring authentication."""
    def wrapper(f):  # pylint: disable=invalid-name
        """Wrap decorated function."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            """Wrap function f."""
            try:
                auth_header = request.headers.get('Authorization')
                if not auth_header:
                    raise NotAuthenticated('Provide a valid auth token.')
                auth_token = auth_header.split(' ')[1]
                user_uuid = decode_auth_token(auth_token)
                user = User.query.filter_by(uuid=user_uuid).first()
                if not user or not user.active:
                    raise AuthenticationFailed('User is not active')
                return f(user_uuid, *args, **kwargs)
            except (NotAuthenticated, AuthenticationFailed):
                if required:
                    raise
                return f(None, *args, **kwargs)
        return decorated_function
    return wrapper
