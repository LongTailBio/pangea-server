"""Analysis Result API endpoint definitions."""

from uuid import UUID

from flask import Blueprint
from flask_api.exceptions import NotFound, ParseError
from mongoengine import DoesNotExist

from app.analysis_results.analysis_result_models import AnalysisResultMeta, analysis_result_schema


analysis_results_blueprint = Blueprint('analysis_results', __name__)  # pylint: disable=invalid-name


@analysis_results_blueprint.route('/analysis_results/<result_uuid>', methods=['GET'])
def get_single_result(result_uuid):
    """Get single analysis result."""
    try:
        uuid = UUID(result_uuid)
        analysis_result = AnalysisResultMeta.objects.get(uuid=uuid)
        result = analysis_result_schema.dump(analysis_result)
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')


@analysis_results_blueprint.route('/analysis_results', methods=['GET'])
def get_all_analysis_results():
    """Get all analysis result models."""
    try:
        analysis_results = AnalysisResultMeta.objects.all()
        result = analysis_result_schema.dump(analysis_results, many=True)
        return result, 200
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')
