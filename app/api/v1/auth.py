"""Authentication API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from flask_api.exceptions import ParseError, NotFound, PermissionDenied
from sqlalchemy import or_, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.api.constants import PAGE_SIZE
from app.api.exceptions import InvalidRequest, InternalError
from app.extensions import db, bcrypt
from app.authentication import (
    User,
    Organization,
    PasswordAuthentication,
)
from app.authentication.helpers import (
    encode_auth_token,
    authenticate,
    fetch_organization,
)


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
        )
        new_user.password_authentication = PasswordAuthentication(password=password)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as integrity_error:
        current_app.logger.exception('There was a problem with registration.')
        db.session.rollback()
        raise InternalError(str(integrity_error))

    # Generate auth token
    auth_token = encode_auth_token(new_user)
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
    password_authentication = getattr(user, 'password_authentication', None)
    password_hash = getattr(password_authentication, 'password', None)
    if password_hash and bcrypt.check_password_hash(password_hash, password):
        auth_token = encode_auth_token(user)
        if auth_token:
            result = {'auth_token': auth_token.decode()}
            return result, 200
    raise NotFound('User does not exist.')


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate()
def logout_user(_):
    """Log user out."""
    return {}, 200


@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate()
def get_user_status(authn):
    """Get user status."""
    user = User.query.filter_by(uuid=authn.sub).first()
    result = user.serializable()
    return result, 200


@auth_blueprint.route('/organizations', methods=['POST'])
@authenticate()
def add_organization(authn):
    """Add organization."""
    try:
        post_data = request.get_json()
        org_name = post_data['name']
        primary_admin = User.from_uuid(authn.sub)
        is_public = post_data.get('is_public', True)
    except NoResultFound:
        raise NotFound('User does not exist')
    except TypeError:
        raise ParseError('Missing organization payload.')
    except KeyError:
        raise ParseError('Invalid organization payload.')
    try:
        org = Organization.from_user(primary_admin, org_name, is_public=is_public)
        return org.serializable(), 201
    except IntegrityError:
        current_app.logger.exception('There was a problem adding an organization.')
        raise InternalError(str(integrity_error))


@auth_blueprint.route('/organizations', methods=['GET'])
def get_organizations():
    """Get all organizations."""
    if 'name' in request.args:
        name_query = request.args.get('name')
        try:
            organization = Organization.from_name(name_query)
        except NoResultFound:
            raise NotFound('Organization does not exist')
        return organization.serializable(), 200

    limit = request.args.get('limit', PAGE_SIZE)
    offset = request.args.get('offset', 0)
    organizations = Organization.query.all()
    organizations = sorted(organizations, key=lambda el: str(User.created_at))
    organizations = organizations[offset:(offset + limit)]
    result = {'organizations': [org.serializable() for org in organizations]}
    return result, 200


@auth_blueprint.route('/organizations/<organization_uuid>', methods=['GET'])
def get_single_organization(organization_uuid):
    """Get single organization details."""
    try:
        org = Organization.from_uuid(UUID(organization_uuid))
        return org.serializable(), 200
    except ValueError:
        raise ParseError('Invalid organization UUID.')
    except NoResultFound:
        raise NotFound('Organization does not exist')


@auth_blueprint.route('/organizations/<organization_uuid>/users', methods=['POST'])
@authenticate()
def add_organization_user(authn, organization_uuid):     # pylint: disable=too-many-return-statements
    """Add user to organization."""
    try:
        post_data = request.get_json()
        organization = Organization.from_uuid(UUID(organization_uuid))
        admin = User.from_uuid(authn.sub)
    except TypeError:
        raise ParseError('Missing membership payload.')
    except ValueError:
        raise ParseError('Invalid organization UUID.')
    except NoResultFound:
        raise NotFound('Organization does not exist')
    try:
        user = User.from_uuid(post_data['user_uuid'])
    except KeyError:
        raise ParseError('Invalid membership payload.')
    except NoResultFound:
        raise NotFound('User does not exist')

    if admin.uuid in organization.admin_uuids():
        if user.uuid in organization.reader_uuids():
            raise InvalidRequest('User is already part of organization.')
        role = post_data.get('role', 'read')
        try:
            organization.add_user(user, role_in_org=role)
            result = {'message': f'${user.username} added to ${organization.name}'}
            return result, 200
        except IntegrityError as integrity_error:
            current_app.logger.exception('IntegrityError encountered.')
            raise InternalError(str(integrity_error))
    raise PermissionDenied('You do not have permission to add a user to that organization.')


@auth_blueprint.route('/organizations/<organization_uuid>/users', methods=['GET'])
@authenticate(required=False)
def get_organization_users(authn, organization_uuid):
    """Get single organization's users."""
    org = Organization.from_uuid(organization_uuid)
    authn_user = User.from_uuid(authn.sub) if authn else None
    if (authn_user and authn_user.uuid in org.reader_uuids()) or org.is_public:
        result = {
            'users': [user.serializable() for user in org.users],
        }
        return result, 200
    raise PermissionDenied('You do not have permission to see that group.')
