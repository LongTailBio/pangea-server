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
from app.authentication.models import (
    User,
    OrganizationMembership,
    PasswordAuthentication,
    user_schema,
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
            user_type='user',
        )
        new_user.password_authentication = PasswordAuthentication(password=password)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as integrity_error:
        current_app.logger.exception('There was a problem with registration.')
        db.session.rollback()
        raise InternalError(str(integrity_error))

    # Generate auth token
    auth_token = encode_auth_token(new_user.uuid)
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
        auth_token = encode_auth_token(user.uuid)
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
    result = {
        'uuid': str(user.uuid),
        'username': user.username,
        'email': user.email,
        'is_deleted': user.is_deleted,
        'created_at': user.created_at
    }
    return result, 200


@auth_blueprint.route('/organizations', methods=['POST'])
@authenticate()
def add_organization(authn):
    """Add organization."""
    try:
        post_data = request.get_json()
        username = post_data['username']
        email = post_data['email']
    except TypeError:
        raise ParseError('Missing organization payload.')
    except KeyError:
        raise ParseError('Invalid organization payload.')

    organization = User.query.filter_by(username=username).first()
    if organization is not None:
        raise InvalidRequest('That name is in use.')

    organization = User.query.filter_by(email=email).first()
    if organization is not None:
        raise InvalidRequest('That email is in use.')

    authn_user = User.query.filter_by(uuid=authn.sub).one()
    try:
        membership = OrganizationMembership(role='admin')
        membership.user = authn_user
        organization = User(username=username, email=email, user_type='organization')
        organization.user_memberships.append(membership)
        db.session.add_all([organization, membership])
        db.session.commit()

        result = user_schema.dump(organization)
        return result, 201
    except IntegrityError as integrity_error:
        current_app.logger.exception('There was a problem adding an organization.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@auth_blueprint.route('/organizations', methods=['GET'])
def get_organizations():
    """Get all organizations."""
    if 'name' in request.args:
        name_query = request.args.get('name')
        try:
            organization = User.query.filter_by(user_type='organization',
                                                username=name_query).one()
        except NoResultFound:
            raise NotFound('Organization does not exist')
        result = user_schema.dump(organization)
        return result, 200

    limit = request.args.get('limit', PAGE_SIZE)
    offset = request.args.get('offset', 0)
    organizations = User.query.filter_by(user_type='organization') \
        .limit(limit) \
        .offset(offset) \
        .order_by(asc(User.created_at)) \
        .all()

    result = user_schema.dump(organizations, many=True)
    return result, 200


@auth_blueprint.route('/organizations/<organization_uuid>', methods=['GET'])
def get_single_organization(organization_uuid):
    """Get single organization details."""
    organization = fetch_organization(organization_uuid)
    result = user_schema.dump(organization)
    return result, 200


@auth_blueprint.route('/organizations/<organization_uuid>/users', methods=['POST'])
@authenticate()
def add_organization_user(authn, organization_uuid):     # pylint: disable=too-many-return-statements
    """Add user to organization."""
    try:
        post_data = request.get_json()
        user_uuid = post_data['user_uuid']
        organization_uuid = UUID(organization_uuid)
    except TypeError:
        raise ParseError('Missing membership payload.')
    except KeyError:
        raise ParseError('Invalid membership payload.')
    except ValueError:
        raise ParseError('Invalid organization UUID.')

    try:
        organization = User.query.filter_by(uuid=organization_uuid).one()
    except NoResultFound:
        raise NotFound('Organization does not exist')

    authn_user = User.query.filter_by(uuid=authn.sub).one()
    try:
        _ = OrganizationMembership.query.filter_by(
            organization_uuid=organization.uuid,
            user_uuid=authn_user.uuid,
            role='admin',
        ).one()
    except NoResultFound:
        message = 'You do not have permission to add a user to that organization.'
        raise PermissionDenied(message)

    try:
        user = User.query.filter_by(uuid=user_uuid).one()
    except NoResultFound:
        raise InvalidRequest('User does not exist')

    membership = OrganizationMembership.query.filter_by(
        organization_uuid=organization.uuid,
        user_uuid=user.uuid,
    ).first()
    if membership:
        raise InvalidRequest('User is already part of organization.')

    try:
        role = post_data.get('role', 'read')
        membership = OrganizationMembership(role=role)
        membership.user = user
        membership.organization = organization
        db.session.add(membership)
        db.session.commit()
        message = f'${user.username} added to ${organization.name}'
        result = {'message': message}
        return result, 200
    except IntegrityError as integrity_error:
        current_app.logger.exception('IntegrityError encountered.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@auth_blueprint.route('/organizations/<organization_uuid>/users', methods=['GET'])
@authenticate(required=False)
def get_organization_users(authn, organization_uuid):
    """Get single organization's users."""
    organization = fetch_organization(organization_uuid)

    authn_user = User.query.filter_by(uuid=authn.sub).one() if authn else None
    if authn_user in organization.users:
        result = user_schema.dump(organization.users, many=True)
        return result, 200

    users = organization.users.filter_by(is_public=True).all()
    result = user_schema.dump(users, many=True)
    return result, 200
