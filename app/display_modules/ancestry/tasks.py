"""Tasks to process Alpha Diversity results."""

from pandas import DataFrame

from app.extensions import celery
from app.display_modules.utils import persist_result_helper

from .models import AncestryResult


@celery.task()
def ancestry_reducer(samples):
    """Wrap collated samples as actual Result type."""
    framed_samples = DataFrame(samples).fillna(0).to_dict()
    result_data = {'samples': framed_samples}
    return result_data


@celery.task(name='ancestry.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Beta Diversity results."""
    result = AncestryResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
