"""Sample Group API endpoint definitions."""

from io import StringIO
from uuid import UUID
from csv import DictReader

from flask import Blueprint, current_app, request
from flask_api.exceptions import ParseError, NotFound, PermissionDenied
from sqlalchemy import func, and_, or_, asc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.db_models import SampleGroup, Sample

from app.api.constants import PAGE_SIZE
from app.api.exceptions import InvalidRequest, InternalError
from app.extensions import db
from app.authentication import User, Organization
from app.authentication.helpers import authenticate, fetch_organization
from app.utils import XLSDictReader


sample_groups_blueprint = Blueprint('sample_groups', __name__)  # pylint: disable=invalid-name


@sample_groups_blueprint.route('/sample_groups', methods=['POST'])
@authenticate()
def add_sample_group(authn):  # pylint: disable=too-many-locals
    """Add sample group."""
    # Validate input
    try:
        data = request.get_json()
        name = data['name']
        organization = Organization.query.filter_by(name=data['organization_name']).first()
    except TypeError as exc:
        current_app.logger.exception(f'Sample Group creation error:\n{exc}')
        raise ParseError(f'Missing Sample Group creation payload.\n{exc}')
    except KeyError:
        raise ParseError('Invalid Sample Group creation payload.')
    authn_user = User.query.filter_by(uuid=authn.sub).first()
    if authn_user.uuid not in organization.writer_uuids():
        raise PermissionDenied('You do not have permission to write to that organization.')

    # Create Sample Group
    try:
        sample_group = SampleGroup(
            name=name,
            organization_uuid=organization.uuid,
            description=data.get('description', False),
            is_library=data.get('is_library', False),
            is_public=data.get('is_public', False),
        ).save()
        return sample_group.serializable(), 201
    except IntegrityError as integrity_error:
        current_app.logger.exception('Sample Group could not be created.')
        raise ParseError('Duplicate group name.')

'''
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
            )).first()
        except NoResultFound:
            raise NotFound('Sample Group does not exist.')

        result = sample_group.serializable()
        return result, 200

    # Return all sample groups
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', PAGE_SIZE)
    sample_groups = SampleGroup.query \
        .order_by(asc(SampleGroup.created_at)) \
        .offset(offset) \
        .limit(limit) \
        .all()

    result = {
        'sample_groups': [sg.serializable() for sg in sample_group.samples],
    }
    return result, 200
'''


@sample_groups_blueprint.route('/sample_groups/<group_uuid>', methods=['GET'])
def get_single_sample_group(group_uuid):
    """Get single sample group model."""
    try:
        sample_group = SampleGroup.query.filter_by(uuid=UUID(group_uuid)).one()
        return sample_group.serializable(), 200
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')

'''
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
'''


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/samples', methods=['GET'])
def get_samples_for_group(group_uuid):
    """Get single sample group's list of samples."""
    try:
        sample_group = SampleGroup.query.filter_by(uuid=UUID(group_uuid)).one()
        result = {
            'samples': [sample.serializable() for sample in sample_group.samples],
        }
        return result, 200
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')



@sample_groups_blueprint.route('/sample_groups/byname/<group_name>/samples', methods=['GET'])
def get_samples_for_group_by_name(group_name):
    """Get single sample group's list of samples."""
    try:
        sample_group = SampleGroup.from_name(group_name)
        result = {
            'samples': [sample.serializable() for sample in sample_group.samples],
        }
        return result, 200
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/samples', methods=['POST'])
@authenticate()
def add_samples_to_group(authn, group_uuid):
    """Add samples to a sample group."""
    try:
        post_data = request.get_json()
        sample_group = SampleGroup.query.filter_by(uuid=UUID(group_uuid)).one()
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')
    authn_user = User.query.filter_by(uuid=authn.sub).first()
    organization = Organization.query.filter_by(uuid=sample_group.organization_uuid).first()
    if authn_user.uuid not in organization.writer_uuids():
        raise PermissionDenied('You do not have permission to write to that organization.')
    for sample_uuid in [UUID(uuid) for uuid in post_data.get('sample_uuids')]:
        try:
            sample = Sample.query.filter_by(uuid=sample_uuid).first()
            sample_group.samples.append(sample)
        except NoResultFound:
            raise InvalidRequest(f'Sample UUID \'{sample_uuid}\' does not exist')
        except IntegrityError as integrity_error:
            current_app.logger.exception(f'Sample \'{sample_uuid}\' could not be added to Sample Group.')
            raise InternalError(str(integrity_error))
    sample_group.save()
    result = sample_group.serializable()
    return result, 200


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


def get_metadata_from_request(request):
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
    return metadata


@sample_groups_blueprint.route('/libraries/<library_uuid>/metadata', methods=['POST'])
@authenticate()
def upload_metadata(_, library_uuid):  # pylint: disable=too-many-branches,too-many-locals
    """Upload metadata for a library."""
    try:
        library = SampleGroup.query.filter_by(uuid=UUID(library_uuid)).first()
    except ValueError:
        raise ParseError('Invalid Library UUID.')
    except NoResultFound:
        raise NotFound('Library does not exist')
    metadata = get_metadata_from_request(request)
    sample_name_col = metadata.fieldnames[0]
    updates, updated_uuids = {}, []
    for row in metadata:
        sample = library.sample(row[sample_name_col])
        sample = sample.set_sample_metadata({
            key: value for key, value in row.items() if key is not sample_name_col
        })
        updated_uuids.append(sample.uuid)

    return {'updated_uuids': updated_uuids}, 201


@sample_groups_blueprint.route('/organizations/<organization_uuid>/sample_groups',
                               methods=['GET'])
def get_organization_sample_groups(organization_uuid):
    """Get single organization's sample groups."""
    offset = request.args.get('offset', 0)
    limit = request.args.get('limit', PAGE_SIZE)
    sample_groups = SampleGroup.query \
        .filter_by(organization_uuid=organization_uuid) \
        .order_by(asc(SampleGroup.created_at)) \
        .offset(offset) \
        .limit(limit) \
        .all()

    result = {
        'sample_groups': [sg.serializable() for sg in sample_groups],
    }
    return result, 200
