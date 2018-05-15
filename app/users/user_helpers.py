"""Helper methods related to User model."""

from functools import wraps

from flask import request
from flask_api.exceptions import NotAuthenticated, AuthenticationFailed

from app.users.user_models import User


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
                user_uuid = User.decode_auth_token(auth_token)
                user = User.query.filter_by(id=user_uuid).first()
                if not user or not user.active:
                    raise AuthenticationFailed('User is not active')
                return f(user_uuid, *args, **kwargs)
            except (NotAuthenticated, AuthenticationFailed):
                if required:
                    raise
                return f(None, *args, **kwargs)
        return decorated_function
    return wrapper
