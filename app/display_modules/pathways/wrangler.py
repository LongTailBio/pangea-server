"""Tasks for generating Pathway results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import jsonify

from .constants import MODULE_NAME
from .tasks import filter_humann2_pathways, persist_result


class PathwayWrangler(DisplayModuleWrangler):
    """Task for generating Pathway results."""

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather single sample and process."""
        samples = [jsonify(sample)]
        persist_task = persist_result.s(sample['analysis_result'], MODULE_NAME)
        task_chain = chain(filter_humann2_pathways.s(samples),
                           persist_task)
        result = task_chain.delay()

        return result

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather samples and process."""
        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)
        task_chain = chain(filter_humann2_pathways.s(samples),
                           persist_task)
        result = task_chain.delay()

        return result
