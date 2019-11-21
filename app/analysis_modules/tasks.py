"""Tasks for the Conductor module."""

# from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.extensions import celery


@celery.task(bind=True)
def clean_error(self):
    """Handle expected error types cleanly.

    To be used like: module_task.s(sample_group_id).on_error(clean_error.s()).delay()
    """
    # Try to get analysis_result.id from parent tasks metadata
    parent_meta = self.parent.result.info
    analysis_result_id = parent_meta['analysis_result_id']
    module_name = parent_meta['module_name']
    analysis_result = AnalysisResultMeta.objects.get(uuid=analysis_result_id)
    wrapper = getattr(analysis_result, module_name).fetch()
    wrapper.status = 'E'
    wrapper.save()
    analysis_result.save()
