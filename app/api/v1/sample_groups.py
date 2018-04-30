"""Sample Group API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from flask_api.exceptions import ParseError, NotFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.api.exceptions import InvalidRequest, InternalError
from app.display_modules import all_display_modules
from app.display_modules.conductor import GroupConductor
from app.extensions import db
from app.sample_groups.sample_group_models import SampleGroup, sample_group_schema
from app.samples.sample_models import Sample, sample_schema
from app.users.user_helpers import authenticate

# from .utils import kick_off_middleware


sample_groups_blueprint = Blueprint('sample_groups', __name__)  # pylint: disable=invalid-name


@sample_groups_blueprint.route('/sample_groups', methods=['POST'])
@authenticate
def add_sample_group(resp):  # pylint: disable=unused-argument
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

    try:
        analysis_result = AnalysisResultMeta().save()
        sample_group = SampleGroup(name=name, analysis_result=analysis_result)
        db.session.add(sample_group)
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


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/samples', methods=['GET'])
def get_samples_for_group(group_uuid):
    """Get single sample group's list of samples."""
    try:
        sample_group_id = UUID(group_uuid)
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
        samples = sample_group.samples
        result = sample_schema.dump(samples, many=True).data
        return result, 200
    except ValueError:
        raise ParseError('Invalid Sample Group UUID.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist')


@sample_groups_blueprint.route('/sample_groups/<group_uuid>/samples', methods=['POST'])
@authenticate
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


@sample_groups_blueprint.route('/sample_groups/<uuid>/middleware', methods=['POST'])
def run_sample_group_display_modules(uuid):    # pylint: disable=invalid-name
    """Run display modules for sample group."""
    try:
        safe_uuid = UUID(uuid)
        _ = SampleGroup.query.filter_by(id=safe_uuid).first()
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except NoResultFound:
        raise NotFound('Sample Group does not exist.')

    for module in all_display_modules:
        try:
            GroupConductor(safe_uuid, display_modules=[module])
        except Exception:  # pylint: disable=broad-except
            current_app.logger.exception('Exception while coordinating display modules.')

    result = {'message': 'Started middleware'}

    return result, 202
