"""Sample Group API endpoint definitions."""

from io import StringIO
from uuid import UUID
from csv import DictReader

from flask import Blueprint, current_app, request
from flask_api.exceptions import ParseError, NotFound, PermissionDenied
from mongoengine.errors import ValidationError, DoesNotExist
from sqlalchemy import func, and_, or_, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.analysis_modules.task_graph import TaskConductor
from app.db_models import SampleGroup

from app.api.constants import PAGE_SIZE
from app.api.exceptions import InvalidRequest, InternalError
from app.extensions import db
from app.authentication.models import User, OrganizationMembership
from app.authentication.helpers import authenticate, fetch_organization
from app.utils import XLSDictReader


sample_groups_blueprint = Blueprint('sample_groups', __name__)  # pylint: disable=invalid-name


@sample_groups_blueprint.route('/sample_groups', methods=['POST'])
@authenticate()
def add_sample_group(authn):  # pylint: disable=too-many-locals
    """Add sample group."""
    # Validate input
    try:
        post_data = request.get_json()
        name = post_data['name']
        organization_name = post_data.get('organization_name', None)
        is_library = post_data.get('is_library', False)
        is_public = post_data.get('is_public', True)
    except TypeError as exc:
        print('Sample Group creation error:')
        print(exc)
        raise ParseError('Missing Sample Group creation payload.')
    except KeyError:
        raise ParseError('Invalid Sample Group creation payload.')

    # Assume Sample Group is self-owned
    authn_user = User.query.filter_by(uuid=authn.sub).one()
    owner_name = authn_user.username
    owner_uuid = authn_user.uuid

    # Validate organization permissions if organization-owned
    if organization_name:
        try:
            organization = User.query.filter(
                func.lower(User.username) == func.lower(organization_name),
            ).one()
        except NoResultFound:
            raise NotFound('Organization does not exist')

        try:
            _ = User.query.filter(
                User.uuid == authn_user.uuid,
                or_(
                    User.organization_memberships.any(
                        organization_uuid=organization.uuid,
                        role='admin',
                    ),
                    User.organization_memberships.any(
                        organization_uuid=organization.uuid,
                        role='write',
                    ),
                ),
            ).one()
        except NoResultFound:
            raise PermissionDenied('You do not have permission to that organization.')

        owner_name = organization.username
        owner_uuid = organization.uuid

    # Check if owner/sample group already exists
    sample_group = SampleGroup.query.filter(and_(
        func.lower(SampleGroup.name) == func.lower(name),
        SampleGroup.owner_uuid == owner_uuid,
    )).first()
    if sample_group:
        raise InvalidRequest('Sample Group with that name already exists.')

    # Create Sample Group
    try:
        sample_group = SampleGroup(
            name=name,
            owner_name=owner_name,
            owner_uuid=owner_uuid,
            is_library=is_library,
            is_public=is_public,
        )
        db.session.add(sample_group)
        db.session.commit()
        result = sample_group_schema.dump(sample_group)
        return result, 201
    except IntegrityError as integrity_error:
        current_app.logger.exception('Sample Group could not be created.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@sample_groups_blueprint.route('/sample_groups', methods=['GET'])
def get_sample_groups():
    """Return the UUID associated with a single sample."""
    # Lookup specific Sample Group if queried
    name_query = request.args.get('name', None)
    owner_name_query = request.args.get('owner_name', None)
    if name_query and owner_name_query:
        # Get owner
        try:
            owner = User.query.filter(
                func.lower(User.username) == func.lower(owner_name_query),
            ).one()
        except NoResultFound:
            raise NotFound('User or organization with that name does not exist.')

        # Get Sample Group
        try:
            sample_group = SampleGroup.query.filter(and_(
                SampleGroup.owner_uuid == owner.uuid,
                func.lower(SampleGroup.name) == func.lower(name_query),
            )).one()
        except NoResultFound:
            raise NotFound('Sample Group does not exist.')

        result = sample_group_schema.dump(sample_group)
        return result, 200

    # Return all sample groups
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', PAGE_SIZE)
    sample_groups = SampleGroup.query \
        .order_by(asc(SampleGroup.created_at)) \
        .offset(offset) \
        .limit(limit) \
        .all()

    result = sample_group_schema.dump(sample_groups, many=True)
    return result, 200


@sample_groups_blueprint.route('/sample_groups/<group_uuid>', methods=['GET'])
def get_single_sample_group(group_uuid):
    """Get single sample group model."""
    # Valdiate input
    try:
        sample_group_uuid = UUID(group_uuid)
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')

    try:
        sample_group = SampleGroup.query.filter_by(uuid=sample_group_uuid).one()
        result = sample_group_schema.dump(sample_group)
        return result, 200
    except NoResultFound:
        raise NotFound('Sample Group does not exist')


@sample_groups_blueprint.route('/sample_groups/<group_uuid>', methods=['DELETE'])
@authenticate()
def delete_single_result(authn, group_uuid):
    """Delete single sample group model."""
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(uuid=sample_group_id).one()
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')

    if authn.sub != sample_group.owner_uuid:
        try:
            _ = OrganizationMembership.query.filter_by(
                organization_uuid=sample_group.owner_uuid,
                user_uuid=authn.sub,
                role='admin',
            ).one()
        except NoResultFound:
            message = 'You do not have permission to delete that sample group.'
            raise PermissionDenied(message)

    try:
        sample_group.analysis_result.delete()
        for row in sample_group.sample_placeholders:
            db.session.delete(row)
        db.session.delete(sample_group)
        db.session.commit()
        return {}, 200
    except IntegrityError as integrity_error:
        current_app.logger.exception('Sample Group could not be deleted.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/samples', methods=['GET'])
def get_samples_for_group(group_uuid):
    """Get single sample group's list of samples."""
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(uuid=sample_group_id).one()
        samples = sample_group.samples
        result = SampleSchema(only=('uuid', 'name')).dump(samples, many=True)
        return result, 200
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/samples', methods=['POST'])
@authenticate()
def add_samples_to_group(_, group_uuid):
    """Add samples to a sample group."""
    try:
        post_data = request.get_json()
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(uuid=sample_group_id).one()
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')

    try:
        sample_uuids = [UUID(uuid) for uuid in post_data.get('sample_uuids')]
        for sample_uuid in sample_uuids:
            sample = Sample.objects.get(uuid=sample_uuid)
            sample_group.sample_uuids.append(sample.uuid)
        db.session.commit()
        result = sample_group_schema.dump(sample_group)
        return result, 200
    except NoResultFound:
        db.session.rollback()
        raise InvalidRequest(f'Sample UUID \'{sample_uuid}\' does not exist')
    except IntegrityError as integrity_error:
        current_app.logger.exception('Samples could not be added to Sample Group.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@sample_groups_blueprint.route('/sample_groups/<uuid>/middleware', methods=['POST'])
def run_sample_group_display_modules(uuid):    # pylint: disable=invalid-name
    """Run display modules for sample group."""
    try:
        safe_uuid = UUID(uuid)
        _ = SampleGroup.query.filter_by(uuid=safe_uuid).first()
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist.')

    analysis_names = request.args.getlist('analysis_names')
    TaskConductor(uuid, analysis_names).shake_that_baton()

    result = {'middleware': analysis_names}

    return result, 202


@sample_groups_blueprint.route('/libraries/<library_uuid>/metadata', methods=['POST'])
@authenticate()
def upload_metadata(_, library_uuid):  # pylint: disable=too-many-branches,too-many-locals
    """Upload metadata for a library."""
    try:
        library_id = UUID(library_uuid)
        # Enforce is_library
        _ = SampleGroup.query.filter_by(uuid=library_id).one()
    except ValueError:
        raise ParseError('Invalid Library UUID.')
    except NoResultFound:
        raise NotFound('Library does not exist')

    try:
        metadata_file = request.files['metadata']
    except KeyError:
        raise ParseError('Missing metadata file attachment.')

    if metadata_file.filename == '':
        raise ParseError('Missing metadata file attachment.')

    try:
        extension = metadata_file.filename.split('.')[1]
    except KeyError:
        raise ParseError('Metadata file missing extension.')

    stream = StringIO(metadata_file.stream.read().decode('UTF8'), newline=None)
    if extension == 'csv':
        metadata = DictReader(stream)
    elif 'xls' in extension:
        metadata = XLSDictReader(stream)
    else:
        raise ParseError('Missing valid metadata file attachment.')

    sample_name_col = metadata.fieldnames[0]
    updates = {}

    for row in metadata:
        sample_name = row[sample_name_col]
        new_metadata = {key: value for key, value in row.items()
                        if key is not sample_name_col}
        updates[sample_name] = new_metadata

    # MongoDB has no transactions so we must do as much as we can upfront to
    # avoid errors; ensure all samples at least exist
    updates_by_uuid = []
    missing_samples = []
    for sample_name in updates:
        try:
            sample = Sample.objects.get(name=sample_name, library_uuid=library_id)
            # Searching by UUID directly will be faster in the actual update phase
            updates_by_uuid.append((sample.uuid, updates[sample_name]))
        except DoesNotExist:
            missing_samples.append(sample_name)
    if missing_samples:
        raise InvalidRequest((f'The following samples do not exist in Library '
                              f'{library_id}: {missing_samples}'))

    # Actually perform the updates
    updated_uuids = []
    for sample_uuid, new_metadata in updates_by_uuid:
        try:
            sample = Sample.objects.get(uuid=sample_uuid)
            sample.metadata = new_metadata
            sample.save()
            updated_uuids.append(str(sample_uuid))
        except ValidationError as validation_error:
            current_app.logger.exception('Sample metadata could not be updated.')
            raise ParseError(f'Metadata upload failed partway through: {str(validation_error)}')

    return {'updated_uuids': updated_uuids}, 201


@sample_groups_blueprint.route('/organizations/<organization_uuid>/sample_groups',
                               methods=['POST'])
@authenticate()
def add_organization_sample_group(authn, organization_uuid):
    """Add sample group to organization."""
    # Validate organization
    organization = fetch_organization(organization_uuid)

    try:
        authn_user = User.query.filter_by(uuid=authn.sub).one()
        _ = OrganizationMembership.query.filter(and_(
            OrganizationMembership.organization_uuid == organization.uuid,
            OrganizationMembership.user_uuid == authn_user.uuid,
            or_(
                OrganizationMembership.role == 'admin',
                OrganizationMembership.role == 'write',
            ),
        )).one()
    except NoResultFound:
        message = 'You do not have permission to add a sample group to that organization.'
        raise PermissionDenied(message)

    # Validate sample group
    try:
        post_data = request.get_json()
        sample_group_uuid = post_data['sample_group_uuid']
        sample_group_uuid = UUID(sample_group_uuid)
        sample_group = SampleGroup.query.filter_by(uuid=sample_group_uuid).one()
    except TypeError:
        raise ParseError('Missing sample group payload.')
    except KeyError:
        raise ParseError('Invalid sample group payload.')
    except ValueError:
        raise ParseError('Invalid sample group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')

    old_owner = sample_group.owner_uuid
    if not old_owner == authn_user.uuid:
        try:
            _ = OrganizationMembership.query.filter(and_(
                OrganizationMembership.organization_uuid == old_owner,
                OrganizationMembership.user_uuid == authn_user.uuid,
                OrganizationMembership.role == 'admin',
            )).one()
        except NoResultFound:
            message = 'You do not have permission edit that sample group.'
            raise PermissionDenied(message)

    # Change ownership
    try:
        sample_group.owner_name = organization.username
        sample_group.owner_uuid = organization.uuid
        db.session.commit()
        result = {'message': f'${sample_group.name} added to ${organization.username}'}
        return result, 200
    except IntegrityError as integrity_error:
        current_app.logger.exception('IntegrityError encountered while saving organization.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@sample_groups_blueprint.route('/organizations/<organization_uuid>/sample_groups',
                               methods=['GET'])
def get_organization_sample_groups(organization_uuid):
    """Get single organization's sample groups."""
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', PAGE_SIZE)
    sample_groups = SampleGroup.query \
        .filter_by(owner_uuid=organization_uuid) \
        .order_by(asc(SampleGroup.created_at)) \
        .offset(offset) \
        .limit(limit) \
        .all()

    result = sample_group_schema.dump(sample_groups, many=True)
    return result, 200
