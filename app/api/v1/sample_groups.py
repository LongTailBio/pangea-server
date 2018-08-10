"""Sample Group API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from flask_api.exceptions import ParseError, NotFound, PermissionDenied
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.api.exceptions import InvalidRequest, InternalError
from app.display_modules import all_display_modules
from app.display_modules.conductor import SampleConductor
from app.extensions import db
from app.organizations.organization_models import Organization
from app.sample_groups.sample_group_models import SampleGroup, sample_group_schema
from app.samples.sample_models import Sample, SampleSchema
from app.users.user_helpers import authenticate

# from .utils import kick_off_middleware


sample_groups_blueprint = Blueprint('sample_groups', __name__)  # pylint: disable=invalid-name


@sample_groups_blueprint.route('/sample_groups', methods=['POST'])
@authenticate()
def add_sample_group(auth_user_uuid):  # pylint: disable=unused-argument
    """Add sample group."""
    try:
        post_data = request.get_json()
        name = post_data['name']
    except TypeError:
        raise ParseError('Missing Sample Group creation payload.')
    except KeyError:
        raise ParseError('Invalid Sample Group creation payload.')

    sample_group = SampleGroup.query.filter_by(name=name).first()
    if sample_group is not None:
        raise InvalidRequest('Sample Group with that name already exists.')

    organization = None
    if 'organization_uuid' in post_data:
        organization_uuid = post_data['organization_uuid']
        try:
            organization = Organization.query.filter_by(id=organization_uuid).one()
        except NoResultFound:
            raise NotFound('Sample Group does not exist')

        user_ids = [user.id for user in organization.users]
        if auth_user_uuid not in user_ids:
            raise PermissionDenied('You do not have permission to that organization.')

    try:
        analysis_result = AnalysisResultMeta().save()
        sample_group = SampleGroup(name=name, analysis_result=analysis_result)
        db.session.add(sample_group)
        if organization:
            organization.sample_groups.append(sample_group)
        db.session.commit()
        result = sample_group_schema.dump(sample_group).data
        return result, 201
    except IntegrityError as integrity_error:
        current_app.logger.exception('Sample Group could not be created.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@sample_groups_blueprint.route('/sample_groups/<group_uuid>', methods=['GET'])
def get_single_result(group_uuid):
    """Get single sample group model."""
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
        result = sample_group_schema.dump(sample_group).data
        return result, 200
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')


@sample_groups_blueprint.route('/sample_groups/<group_uuid>', methods=['DELETE'])
def delete_single_result(group_uuid):
    """Delete single sample group model."""
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
        db.session.delete(sample_group)
        db.session.commit()
        return {}, 200
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')
    except IntegrityError as integrity_error:
        current_app.logger.exception('Sample Group could not be deleted.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/samples', methods=['GET'])
def get_samples_for_group(group_uuid):
    """Get single sample group's list of samples."""
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
        samples = sample_group.samples
        current_app.logger.info(f'Found {len(samples)} samples for group {group_uuid}')
        result = SampleSchema(only=('uuid', 'name')).dump(samples, many=True).data
        return result, 200
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/samples', methods=['POST'])
@authenticate()
def add_samples_to_group(resp, group_uuid):  # pylint: disable=unused-argument
    """Add samples to a sample group."""
    try:
        post_data = request.get_json()
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')

    try:
        sample_uuids = [UUID(uuid) for uuid in post_data.get('sample_uuids')]
        for sample_uuid in sample_uuids:
            sample = Sample.objects.get(uuid=sample_uuid)
            sample_group.sample_ids.append(sample.uuid)
        db.session.commit()
        result = sample_group_schema.dump(sample_group).data
        return result, 200
    except NoResultFound:
        db.session.rollback()
        raise InvalidRequest(f'Sample UUID \'{sample_uuid}\' does not exist')
    except IntegrityError as integrity_error:
        current_app.logger.exception('Samples could not be added to Sample Group.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@sample_groups_blueprint.route('/sample_groups/getid/<sample_group_name>', methods=['GET'])
def get_sample_group_uuid(sample_group_name):
    """Return the UUID associated with a single sample."""
    try:
        sample_group = SampleGroup.query.filter_by(name=sample_group_name).one()
    except NoResultFound:
        raise NotFound('Sample Group does not exist')

    sample_group_uuid = sample_group.id
    result = {
        'sample_group_name': sample_group_name,  # recapitulate for convenience
        'sample_group_uuid': sample_group_uuid,
    }
    return result, 200


@sample_groups_blueprint.route('/sample_groups/<uuid>/middleware', methods=['POST'])
def run_sample_group_display_modules(uuid):    # pylint: disable=invalid-name
    """Run display modules for sample group."""
    try:
        safe_uuid = UUID(uuid)
        group = SampleGroup.query.filter_by(id=safe_uuid).first()
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist.')

    for module in all_display_modules:
        try:
            SampleConductor('', display_modules=[module]).direct_sample_group(group)
        except Exception:  # pylint: disable=broad-except
            current_app.logger.exception('Exception while coordinating display modules.')

    result = {'message': 'Started middleware'}

    return result, 202
