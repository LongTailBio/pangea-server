"""Authentication API endpoint definitions."""

from flask import Blueprint, current_app, request
from flask_api.exceptions import ParseError, NotFound
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from app.api.exceptions import InvalidRequest, InternalError
from app.extensions import db, bcrypt
from app.users.user_models import User
from app.users.user_helpers import authenticate


auth_blueprint = Blueprint('auth', __name__)  # pylint: disable=invalid-name


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    """Register user."""
    try:
        post_data = request.get_json()
        username = post_data['username']
        email = post_data['email']
        password = post_data['password']
    except TypeError:
        raise ParseError('Missing registration payload.')
    except KeyError:
        raise ParseError('Invalid registration payload.')

    # Check for existing user
    user = User.query.filter(or_(User.username == username,
                                 User.email == email)).first()
    if user is not None:
        raise InvalidRequest('Sorry. That user already exists.')

    try:
        # Add new user to db
        new_user = User(
            username=username,
            email=email,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as integrity_error:
        current_app.logger.exception('There was a problem with registration.')
        db.session.rollback()
        raise InternalError(str(integrity_error))

    # Generate auth token
    auth_token = new_user.encode_auth_token(new_user.id)
    result = {'auth_token': auth_token.decode()}
    return result, 201


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    """Log user in."""
    try:
        post_data = request.get_json()
        email = post_data['email']
        password = post_data['password']
    except TypeError:
        raise ParseError('Missing login payload.')
    except KeyError:
        raise ParseError('Invalid login payload.')

    # Fetch the user data
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        auth_token = user.encode_auth_token(user.id)
        if auth_token:
            result = {'auth_token': auth_token.decode()}
            return result, 200
    raise NotFound('User does not exist.')


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate()
def logout_user(resp):  # pylint: disable=unused-argument
    """Log user out."""
    return {}, 200


@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate()
def get_user_status(resp):
    """Get user status."""
    user = User.query.filter_by(id=resp).first()
    result = {
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'active': user.active,
        'created_at': user.created_at
    }
    return result, 200
