"""Organization API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, current_app, request
from flask_api.exceptions import NotFound, ParseError
from mongoengine.errors import ValidationError, DoesNotExist
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from app.extensions import db
from app.analysis_modules.task_graph import TaskConductor
from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.api.exceptions import InvalidRequest, InternalError
from app.samples.sample_models import Sample, SampleSchema, sample_schema
from app.sample_groups.sample_group_models import SampleGroup
from app.authentication.helpers import authenticate


samples_blueprint = Blueprint('samples', __name__)    # pylint: disable=invalid-name


@samples_blueprint.route('/samples', methods=['POST'])
@authenticate()
def add_sample(_):
    """Add sample."""
    try:
        post_data = request.get_json()
        library_uuid = post_data['library_uuid']
        sample_name = post_data['name']
    except TypeError:
        raise ParseError('Missing Sample creation payload.')
    except KeyError:
        raise ParseError('Invalid Sample creation payload.')

    try:
        library = SampleGroup.query.filter_by(uuid=library_uuid).one()
    except NoResultFound:
        raise InvalidRequest('Sample Group does not exist!')

    sample = Sample.objects(name=sample_name).first()
    if sample is not None:
        raise InvalidRequest('A Sample with that name already exists.')

    try:
        analysis_result = AnalysisResultMeta().save()
        sample = Sample(library_uuid=library_uuid,
                        name=sample_name,
                        analysis_result=analysis_result,
                        metadata={'name': sample_name}).save()
        library.sample_uuids.append(sample.uuid)
        db.session.commit()
        result = sample_schema.dump(sample)
        return result, 201
    except ValidationError as validation_error:
        current_app.logger.exception('Sample could not be created.')
        raise InternalError(str(validation_error))
    except IntegrityError as integrity_error:
        current_app.logger.exception('Sample could not be added to Sample Group.')
        db.session.rollback()
        raise InternalError(str(integrity_error))


@samples_blueprint.route('/samples', methods=['GET'])
@authenticate()
def get_all_samples(auth_user_id):  # pylint: disable=unused-argument
    """Get all samples that the user is allowed to see."""
    samples = Sample.objects.query.all()
    fields = ('uuid', 'name', 'created_at')
    result = SampleSchema(only=fields).dump(samples, many=True)
    return result, 200


@samples_blueprint.route('/samples/<sample_uuid>', methods=['GET'])
def get_single_sample(sample_uuid):
    """Get single sample details."""
    try:
        uuid = UUID(sample_uuid)
        sample = Sample.objects.get(uuid=uuid)
        fields = ('uuid', 'name', 'analysis_result_uuid', 'created_at')
        result = SampleSchema(only=fields).dump(sample)
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')


@samples_blueprint.route('/samples/<sample_uuid>/metadata', methods=['GET'])
def get_single_sample_metadata(sample_uuid):
    """Get single sample metadata."""
    try:
        uuid = UUID(sample_uuid)
        sample = Sample.objects.get(uuid=uuid)
        fields = ('uuid', 'name', 'metadata')
        result = SampleSchema(only=fields).dump(sample)
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Sample does not exist.')


@samples_blueprint.route('/samples/metadata', methods=['POST'])
@authenticate()
def add_sample_metadata(_):
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
        result = sample_schema.dump(sample)
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

    analysis_names = request.args.getlist('analysis_names')
    TaskConductor(uuid, analysis_names).shake_that_baton()

    result = {'middleware': analysis_names}

    return result, 202
