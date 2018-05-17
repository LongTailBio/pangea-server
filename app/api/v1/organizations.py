"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from flask_api.exceptions import ParseError, NotFound, PermissionDenied
from sqlalchemy import asc, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.api.constants import PAGE_SIZE
from app.api.exceptions import InvalidRequest, InternalError
from app.extensions import db
from app.organizations.organization_models import (
    Organization, OrganizationMembership, organization_schema
)
from app.users.user_models import User, user_schema
from app.users.user_helpers import authenticate
from app.sample_groups.sample_group_models import SampleGroup, sample_group_schema


organizations_blueprint = Blueprint('organizations', __name__)  # pylint: disable=invalid-name


@organizations_blueprint.route('/organizations', methods=['POST'])
@authenticate()
def add_organization(resp):  # pylint: disable=unused-argument
    """Add organization."""
    try:
        post_data = request.get_json()
        name = post_data['name']
        admin_email = post_data['admin_email']
    except TypeError:
        raise ParseError('Missing organization payload.')
    except KeyError:
        raise ParseError('Invalid organization payload.')

    organization = Organization.query.filter_by(name=name).first()
    if organization is not None:
        raise InvalidRequest('An organization with that name already exists.')

    try:
        packed_params = {'name': name, 'admin_email': admin_email}
        if 'access_scheme' in post_data:
            packed_params['access_scheme'] = post_data['access_scheme']
        db.session.add(Organization(**packed_params))
        db.session.commit()
        result = {'message': f'{name} was added!'}
        return result, 201
    except IntegrityError as integrity_error:
        current_app.logger.exception('There was a problem adding an organization.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@organizations_blueprint.route('/organizations/<organization_uuid>', methods=['GET'])
def get_single_organization(organization_uuid):
    """Get single organization details."""
    try:
        organization_id = UUID(organization_uuid)
    except ValueError:
        raise ParseError('Invalid organization UUID.')

    try:
        organization = Organization.query.filter_by(id=organization_id).one()
    except NoResultFound:
        raise NotFound('Organization does not exist')

    result = organization_schema.dump(organization).data
    return result, 200


@organizations_blueprint.route('/organizations/<organization_uuid>/users', methods=['GET'])
def get_organization_users(organization_uuid):
    """Get single organization's users."""
    try:
        organization_id = UUID(organization_uuid)
    except ValueError:
        raise ParseError('Invalid organization UUID.')

    try:
        organization = Organization.query.filter_by(id=organization_id).one()
    except NoResultFound:
        raise NotFound('Organization does not exist')

    result = user_schema.dump(organization.users, many=True).data
    return result, 200


@organizations_blueprint.route('/organizations/<organization_uuid>/users', methods=['POST'])
@authenticate()
def add_organization_user(resp, organization_uuid):     # pylint: disable=too-many-return-statements
    """Add user to organization."""
    try:
        post_data = request.get_json()
        user_id = post_data['user_id']
        organization_id = UUID(organization_uuid)
    except TypeError:
        raise ParseError('Missing membership payload.')
    except KeyError:
        raise ParseError('Invalid membership payload.')
    except ValueError:
        raise ParseError('Invalid organization UUID.')

    try:
        organization = Organization.query.filter_by(id=organization_id).one()
    except NoResultFound:
        raise NotFound('Organization does not exist')

    auth_user = User.query.filter_by(id=resp).first()
    if not auth_user or auth_user not in organization.admin_users:
        if len(organization.users) or auth_user.email != admin_email:
            message = 'You do not have permission to add a user to that group.'
            raise PermissionDenied(message)

    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise InvalidRequest('User does not exist')

    try:
        organization.users.append(user)
        db.session.commit()
        message = f'${user.username} added to ${organization.name}'
        result = {'message': message}
        return result, 200
    except IntegrityError as integrity_error:
        current_app.logger.exception('IntegrityError encountered.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@organizations_blueprint.route('/organizations/<organization_uuid>/sample_groups',
                               methods=['POST'])
@authenticate()
def add_organization_sample_group(resp, organization_uuid):
    """Add sample group to organization."""
    try:
        organization_id = UUID(organization_uuid)
        organization = Organization.query.filter_by(id=organization_id).one()
    except ValueError:
        raise ParseError('Invalid organization UUID.')
    except NoResultFound:
        raise NotFound('Organization does not exist')

    auth_user = User.query.filter_by(id=resp).first()
    if not auth_user or auth_user not in organization.users:
        message = 'You do not have permission to add a sample group to that organization.'
        raise PermissionDenied(message)

    try:
        post_data = request.get_json()
        sample_group_uuid = UUID(post_data['sample_group_uuid'])
        sample_group = SampleGroup.query.filter_by(id=sample_group_uuid).one()
    except TypeError:
        raise ParseError('Missing sample group payload.')
    except KeyError:
        raise ParseError('Invalid sample group payload.')
    except ValueError:
        raise ParseError('Invalid sample group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')

    try:
        organization.sample_groups.append(sample_group)
        db.session.commit()
        result = {'message': f'${sample_group.name} added to ${organization.name}'}
        return result, 200
    except IntegrityError as integrity_error:
        current_app.logger.exception('IntegrityError encountered while saving organization.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@organizations_blueprint.route('/organizations/<organization_uuid>/sample_groups',
                               methods=['GET'])
@organizations_blueprint.route('/organizations/<organization_uuid>/sample_groups/<int:page>',
                               methods=['GET'])
def get_organization_sample_groups(organization_uuid, page=1):
    """Get single organization's sample groups."""
    try:
        organization_id = UUID(organization_uuid)
    except ValueError:
        raise ParseError('Invalid organization UUID.')

    try:
        organization = Organization.query.filter_by(id=organization_id).one()
    except NoResultFound:
        raise NotFound('Organization does not exist')

    sample_groups = organization.sample_groups.paginate(page, PAGE_SIZE, False).items
    result = sample_group_schema.dump(sample_groups, many=True).data
    return result, 200


@organizations_blueprint.route('/organizations', methods=['GET'])
@authenticate(required=False)
def get_all_organizations(auth_user_id):
    """Get all organizations."""
    if not auth_user_id:
        organizations = Organization.query.filter_by(access_scheme='public').all()
        result = organization_schema.dump(organizations, many=True).data
        return result, 200

    organizations = db.session.query(Organization) \
        .outerjoin(OrganizationMembership) \
        .outerjoin(User) \
        .filter(or_(Organization.access_scheme == 'public',
                    User.id == auth_user_id)) \
        .order_by(asc(Organization.created_at)) \
        .all()

    result = organization_schema.dump(organizations, many=True).data
    return result, 200
