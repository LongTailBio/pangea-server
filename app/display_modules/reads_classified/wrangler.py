"""Tasks for generating Reads Classified results."""

from celery import chain

from app.extensions import celery
from app.display_modules.display_wrangler import SharedWrangler
from app.display_modules.utils import collate_samples, persist_result_helper

from .constants import MODULE_NAME, TOOL_MODULE_NAME
from .models import ReadsClassifiedResult


@celery.task(name='reads_classified.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Reads Classified result."""
    result = ReadsClassifiedResult(samples=result_data)
    persist_result_helper(result, analysis_result_id, result_name)


class ReadsClassifiedWrangler(SharedWrangler):
    """Task for generating Reads Classified results."""

    @classmethod
    def run_common(cls, samples, analysis_result_uuid):
        """Execute common run instructions."""
        collate_fields = ['total', 'viral', 'archaeal', 'bacterial', 'host',
                          'nonhost_macrobial', 'fungal', 'nonfungal_eukaryotic',
                          'unknown']
        collate_task = collate_samples.s(TOOL_MODULE_NAME, collate_fields, samples)
        persist_task = persist_result.s(analysis_result_uuid, MODULE_NAME)

        task_chain = chain(collate_task, persist_task)
        result = task_chain.delay()

        return result
