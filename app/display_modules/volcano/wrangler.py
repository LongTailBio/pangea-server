"""Tasks for generating Volcano results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import categories_from_metadata

from .constants import MODULE_NAME
from .tasks import make_volcanos, persist_result


class VolcanoWrangler(DisplayModuleWrangler):
    """Task for generating Volcano results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        categories_task = categories_from_metadata.s(samples, min_size=1)
        volcano_task = make_volcanos.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)
        task_chain = chain(
            categories_task,
            volcano_task,
            persist_task,
        )
        result = task_chain.delay()

        return result
