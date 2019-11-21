"""Analysis Result API endpoint definitions."""

from uuid import UUID

from flask import Blueprint
from flask_api.exceptions import NotFound, ParseError
from mongoengine import DoesNotExist

from app.db_models import AnalysisResult


analysis_results_blueprint = Blueprint('analysis_results', __name__)  # pylint: disable=invalid-name


@analysis_results_blueprint.route('/analysis_results/<result_uuid>', methods=['GET'])
def get_single_result(result_uuid):
    """Get single analysis result."""
    try:
        uuid = UUID(result_uuid)
        analysis_result = AnalysisResult.get(uuid)
        result = analysis_result.serialize()
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')


@analysis_results_blueprint.route('/analysis_results', methods=['GET'])
def get_all_analysis_results():
    """Get all analysis result models."""
    try:
        analysis_results = AnalysisResult.all()
        result = [ar.serialize() for ar in analysis_results]
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')
