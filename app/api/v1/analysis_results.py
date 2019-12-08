"""Analysis Result API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, request
from flask_api.exceptions import NotFound, ParseError
from sqlalchemy.orm.exc import NoResultFound
from mongoengine import DoesNotExist

from app.db_models import (
    SampleAnalysisResult,
    SampleGroupAnalysisResult,
    SampleGroup,
    Sample,
)


analysis_results_blueprint = Blueprint('analysis_results', __name__)  # pylint: disable=invalid-name


def get_analysis_result(uuid):
    uuid = UUID(uuid)
    analysis_result = SampleAnalysisResult.query.filter_by(uuid=uuid).first()
    if not analysis_result:
        analysis_result = SampleGroupAnalysisResult.query.filter_by(uuid=uuid).first()
    return analysis_result


@analysis_results_blueprint.route('/analysis_results/<result_uuid>/<field_name>', methods=['GET'])
def get_single_result_field(result_uuid, field_name):
    """Get a single field analysis result."""
    try:
        analysis_result = get_analysis_result(result_uuid)
        result = analysis_result.field(field_name).serializable()
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')


@analysis_results_blueprint.route('/analysis_results/<result_uuid>', methods=['GET'])
def get_single_result(result_uuid):
    """Get single analysis result."""
    try:
        analysis_result = get_analysis_result(result_uuid)
        result = analysis_result.serializable()
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')


@analysis_results_blueprint.route('/analysis_results', methods=['GET'])
def get_all_analysis_results():
    """Get all analysis result models."""
    try:
        result = [ar.serializable() for ar in SampleAnalysisResult.all()]
        result += [ar.serializable() for ar in SampleGroupAnalysisResult.all()]
        return result, 200
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')


BY_NAME_URL = '/analysis_results/byname/<lib_name>/<sample_name>/<module_name>'


@analysis_results_blueprint.route(BY_NAME_URL, methods=['GET'])
def get_analysis_result_fields_by_name(lib_name, sample_name, module_name):
    """Get all fields of the specified analysis result."""
    try:
        library = SampleGroup.from_name(lib_name)
        sample = Sample.from_name_library(sample_name, library.uuid)
        analysis_result = SampleAnalysisResult.from_name_sample(module_name, sample.uuid)
        result = {
            field.field_name: field.data
            for field in analysis_result.module_fields
        }
        return result, 200
    except NoResultFound:
        raise NotFound('Analysis Result does not exist.')


@analysis_results_blueprint.route(BY_NAME_URL + '/<field_name>/s3uri', methods=['GET'])
def get_s3_uri_for_specified_analyis_result_field(lib_name, sample_name, module_name, field_name):
    """Get an S3 URI for the specified AR field.

    This S3 URI will not point to an actual file at first.
    Just create a consistent interface for storage
    """
    assert False
    ext = request.args.get('ext', '')


@analysis_results_blueprint.route(BY_NAME_URL + '/<field_name>', methods=['POST'])
def post_analysis_result_field_by_name(lib_name, sample_name, module_name, field_name):
    """Store the payload in the specified analysis result field."""
    assert False
