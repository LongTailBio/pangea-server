"""Handle API registration of AnalysisModules."""

from uuid import UUID
import json

from flask_api.exceptions import NotFound, ParseError

from app.api.exceptions import InvalidRequest
from app.db_models import (
    Sample,
    SampleGroup,
    SampleAnalysisResult,
    SampleGroupAnalysisResult,
)


def get_analysis_results(parent_uuid):
    try:
        Sample.from_uuid(parent_uuid)
        return SampleAnalysisResult.query \
            .filter_by(sample_uuid=parent_uuid) \
            .all()
    except NotFound:
        SampleGroup.from_uuid(parent_uuid)
        return SampleGroupAnalysisResult.query \
            .filter_by(sample_uuid=parent_uuid) \
            .all()


def get_result(display_module, parent_uuid, field=None):
    """Define handler for API requests that defers to display module type."""
    try:
        analysis_results = get_analysis_results(UUID(parent_uuid))
        analysis_results = {ar.module_name: ar for ar in analysis_results}
        analysis_result = analysis_results[display_module.name()]
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except NotFound:
        raise NotFound(f'No analysis result for parent uuid {parent_uuid} found.')
    except KeyError:
        raise InvalidRequest(f'{display_module.name()} is not found.')
    result = {
        key: value for key, value in analysis_result.serializable().items()
        if not key[0:1] == '_'
    }
    for transmission_hook in display_module.transmission_hooks():
        result = transmission_hook(result)

    return result, 200


def get_result_field(display_module, parent_uuid, field_name):
    """Define handler for API requests that defers to display module type."""
    try:
        analysis_results = get_analysis_results(UUID(parent_uuid))
        analysis_results = {ar.module_name: ar for ar in analysis_results}
        analysis_result_field = analysis_results[display_module.name()].field(field_name)
    except ValueError:
        raise ParseError('Invalid UUID provided.')
    except NotFound:
        raise NotFound(f'No analysis result for parent uuid {parent_uuid} found.')
    except KeyError:
        raise InvalidRequest(f'{display_module.name()} is not found.')
    result = {
        key: value for key, value in analysis_result_field.serializable().items()
        if not key[0:1] == '_'
    }
    return result, 200


def register_display_module(display_module, router):
    """Register API endpoint for this display module type."""
    router.add_url_rule(
        f'/analysis_results/<parent_uuid>/{display_module.name()}',
        f'get_{display_module.name()}',
        lambda parent_uuid: get_result(display_module, parent_uuid),
        methods=['GET']
    )
    router.add_url_rule(
        f'/analysis_results/<parent_uuid>/{display_module.name()}/<field_name>',
        f'get_field_{display_module.name()}',
        lambda parent_uuid, field_name: get_result_field(
            display_module, parent_uuid, field_name
        ),
        methods=['GET']
    )
