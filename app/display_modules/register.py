"""Handle API registration of display modules."""

from uuid import UUID

from flask_api.exceptions import NotFound, ParseError
from mongoengine.errors import DoesNotExist

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.api.exceptions import InvalidRequest

from .utils import jsonify


def get_result(cls, result_uuid):
    """Define handler for API requests that defers to display module type."""
    try:
        uuid = UUID(result_uuid)
        analysis_result = AnalysisResultMeta.objects.get(uuid=uuid)
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')

    if cls.name() not in analysis_result:
        raise InvalidRequest(f'{cls.name()} is not in this AnalysisResult.')

    module_results = getattr(analysis_result, cls.name()).fetch()
    result = cls.get_data(module_results)
    # Conversion to dict is necessary to avoid object not callable TypeError
    result_dict = jsonify(result)
    return result_dict, 200


def register_display_module(cls, router):
    """Register API endpoint for this display module type."""
    endpoint_url = f'/analysis_results/<result_uuid>/{cls.name()}'
    endpoint_name = f'get_{cls.name()}'

    def view_function(result_uuid):
        """Wrap get_result to provide class."""
        return get_result(cls, result_uuid)

    router.add_url_rule(endpoint_url,
                        endpoint_name,
                        view_function,
                        methods=['GET'])
