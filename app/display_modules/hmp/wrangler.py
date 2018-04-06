"""Tasks for generating HMP results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import categories_from_metadata, persist_result
from app.sample_groups.sample_group_models import SampleGroup

from .constants import MODULE_NAME
from .tasks import make_distributions, reducer_task


class HMPWrangler(DisplayModuleWrangler):
    """Task for generating HMP results."""

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()
        sample_group.set_module_status(MODULE_NAME, 'W')
        samples = sample_group.samples

        categories_task = categories_from_metadata.s(samples)
        distribution_task = make_distributions.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)
        task_chain = chain(
            categories_task,
            distribution_task,
            reducer_task.s(),
            persist_task
        )
        result = task_chain.delay()

        return result
