"""Helper methods related to User model."""

from functools import wraps

import datetime
import uuid
import jwt

from flask import request, current_app
from flask_api.exceptions import ParseError, NotFound, NotAuthenticated, AuthenticationFailed
from sqlalchemy.orm.exc import NoResultFound

from app.authentication.models import User


def encode_auth_token(user):
    """Generate the auth token."""
    days = current_app.config.get('TOKEN_EXPIRATION_DAYS')
    seconds = current_app.config.get('TOKEN_EXPIRATION_SECONDS')
    now = datetime.datetime.utcnow()
    expires = now + datetime.timedelta(days=days, seconds=seconds)

    memberships = [{
        'uuid': membership.organization_uuid,
        'name': membership.organization.name,
        'roles': membership.role,
    } for membership in user.organization_memberships]

    payload = {
        'exp': expires,
        'iat': datetime.datetime.utcnow(),
        'sub': str(user.uuid),
        'membership': memberships,
    }

    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS512',
    )


class Authn:  # pylint: disable=too-few-public-methods
    """Portable authorization utility class."""

    def __init__(self, auth_token):
        """Create an Authn instance from a JWT string."""
        super(Authn, self).__init__()
        secret = current_app.config.get('SECRET_KEY')
        self.payload = jwt.decode(auth_token, secret, algorithms=['HS512'])
        self.sub = uuid.UUID(self.payload['sub'])


# Decode to "AuthManager" type allowing easier interogation of memberships
def decode_auth_token(auth_token):
    """Decode the auth token - :param auth_token: - :return: UUID|string."""
    try:
        return Authn(auth_token)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Signature expired. Please log in again.')
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token. Please log in again.')


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
                authn = decode_auth_token(auth_token)
                user = User.query.filter_by(uuid=authn.sub).first()
                if not user or user.is_deleted:
                    raise AuthenticationFailed('User is not active')
                return f(authn, *args, **kwargs)
            except (NotAuthenticated, AuthenticationFailed):
                if required:
                    raise
                return f(None, *args, **kwargs)
        return decorated_function
    return wrapper


def fetch_organization(organization_uuid):
    """Get organization from UUID string."""
    try:
        organization_uuid = uuid.UUID(organization_uuid)
        organization = User.query.filter_by(uuid=organization_uuid).one()
        return organization
    except ValueError:
        raise ParseError('Invalid organization UUID.')
    except NoResultFound:
        raise NotFound('Organization does not exist')
