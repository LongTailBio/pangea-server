"""Analysis Result API endpoint definitions."""

from uuid import UUID

from flask import Blueprint, jsonify
from flask_api.exceptions import NotFound, ParseError
from mongoengine import DoesNotExist

from app.db_models import SampleAnalysisResult, SampleGroupAnalysisResult


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
