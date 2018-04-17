"""Tasks for generating Microbe Directory results."""

from app.extensions import celery
from app.display_modules.utils import persist_result_helper

from .models import MicrobeDirectoryResult


@celery.task()
def microbe_directory_reducer(samples):
    """Wrap collated samples as actual Result type."""
    result_data = {'samples': samples}
    return result_data


@celery.task(name='microbe_directory.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Microbe Directory results."""
    result = MicrobeDirectoryResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
