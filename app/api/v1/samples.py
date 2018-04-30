"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from flask_api.exceptions import NotFound, ParseError
from mongoengine.errors import ValidationError, DoesNotExist
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.api.exceptions import InvalidRequest, InternalError
from app.display_modules.conductor import SampleConductor
from app.extensions import db
from app.samples.sample_models import Sample, sample_schema
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results import all_tool_results
from app.tool_results.modules import SampleToolResultModule
from app.users.user_helpers import authenticate

from .utils import kick_off_middleware


samples_blueprint = Blueprint('samples', __name__)    # pylint: disable=invalid-name


@samples_blueprint.route('/samples', methods=['POST'])
@authenticate
def add_sample(resp):  # pylint: disable=unused-argument
    """Add sample."""
    try:
        post_data = request.get_json()
        sample_group_uuid = post_data['sample_group_uuid']
        sample_name = post_data['name']
    except TypeError:
        raise ParseError('Missing Sample creation payload.')
    except KeyError:
        raise ParseError('Invalid Sample creation payload.')

    try:
        sample_group = SampleGroup.query.filter_by(id=sample_group_uuid).one()
    except NoResultFound:
        raise InvalidRequest('Sample Group does not exist!')

    sample = Sample.objects(name=sample_name).first()
    if sample is not None:
        raise InvalidRequest('A Sample with that name already exists.')

    try:
        analysis_result = AnalysisResultMeta().save()
        sample = Sample(name=sample_name,
                        analysis_result=analysis_result,
                        metadata={'name': sample_name}).save()
        sample_group.sample_ids.append(sample.uuid)
        db.session.commit()
        result = sample_schema.dump(sample).data
        return result, 201
    except ValidationError as validation_error:
        current_app.logger.exception('Sample could not be created.')
        raise InternalError(str(validation_error))
    except IntegrityError as integrity_error:
        current_app.logger.exception('Sample could not be added to Sample Group.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@samples_blueprint.route('/samples/<sample_uuid>', methods=['GET'])
def get_single_sample(sample_uuid):
    """Get single sample details."""
    try:
        uuid = UUID(sample_uuid)
        sample = Sample.objects.get(uuid=uuid)
        result = sample_schema.dump(sample).data
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')


@samples_blueprint.route('/samples/metadata', methods=['POST'])
@authenticate
def add_sample_metadata(resp):  # pylint: disable=unused-argument
    """Update metadata for sample."""
    try:
        post_data = request.get_json()
        sample_name = post_data['sample_name']
        metadata = post_data['metadata']
    except TypeError:
        raise ParseError('Missing Sample metadata payload.')
    except KeyError:
        raise ParseError('Invalid Sample metadata payload.')

    try:
        sample = Sample.objects.get(name=sample_name)
    except DoesNotExist:
        raise NotFound('Sample does not exist.')

    try:
        sample.metadata = metadata
        sample.save()
        result = sample_schema.dump(sample).data
        return result, 200
    except ValidationError as validation_error:
        current_app.logger.exception('Sample metadata could not be updated.')
        raise ParseError(f'Invalid Sample metadata payload: {str(validation_error)}')


@samples_blueprint.route('/samples/getid/<sample_name>', methods=['GET'])
def get_sample_uuid(sample_name):
    """Return the UUID associated with a single sample."""
    try:
        sample = Sample.objects.get(name=sample_name)
    except DoesNotExist:
        raise NotFound('Sample does not exist.')

    sample_uuid = sample.uuid
    result = {
        'sample_name': sample_name,  # recapitulate for convenience
        'sample_uuid': sample_uuid,
    }
    return result, 200


@samples_blueprint.route('/samples/<uuid>/middleware', methods=['POST'])
def run_sample_display_modules(uuid):
    """Run display modules for samples."""
    try:
        safe_uuid = UUID(uuid)
        _ = Sample.objects.get(uuid=safe_uuid)
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')

    valid_tools = [tool for tool in all_tool_results
                   if issubclass(tool, SampleToolResultModule)]

    return kick_off_middleware(safe_uuid, request, valid_tools, SampleConductor)
