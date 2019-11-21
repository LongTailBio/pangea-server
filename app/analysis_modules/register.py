"""Handle API registration of AnalysisModules."""

from uuid import UUID
import json

from flask_api.exceptions import NotFound, ParseError
from mongoengine.errors import DoesNotExist

from app.api.exceptions import InvalidRequest


def get_result(display_module, result_uuid):
    """Define handler for API requests that defers to display module type."""
    try:
        uuid = UUID(result_uuid)
        analysis_result = None # AnalysisResultMeta.objects.get(uuid=uuid)
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except DoesNotExist:
        raise NotFound('Analysis Result does not exist.')

    if display_module.name() not in analysis_result:
        raise InvalidRequest(f'{display_module.name()} is not in this AnalysisResult.')

    module_results = getattr(analysis_result, display_module.name()).fetch()
    result = json.loads(module_results.to_json())
    # Strip private fields
    result = {key: value for key, value in result.items() if not key[0:1] == '_'}
    for transmission_hook in display_module.transmission_hooks():
        result = transmission_hook(result)

    return result, 200


def register_display_module(display_module, router):
    """Register API endpoint for this display module type."""
    endpoint_url = f'/analysis_results/<result_uuid>/{display_module.name()}'
    endpoint_name = f'get_{display_module.name()}'

    def view_function(result_uuid):
        """Wrap get_result to provide class."""
        return get_result(display_module, result_uuid)

    router.add_url_rule(endpoint_url,
                        endpoint_name,
                        view_function,
                        methods=['GET'])
