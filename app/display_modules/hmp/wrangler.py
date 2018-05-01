"""Tasks for generating HMP results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import jsonify, categories_from_metadata

from .constants import MODULE_NAME
from .tasks import make_distributions, persist_result


class HMPWrangler(DisplayModuleWrangler):
    """Task for generating HMP results."""

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather single sample and process."""
        samples = [jsonify(sample)]
        categories_task = categories_from_metadata.s(samples, min_size=1)
        distribution_task = make_distributions.s(samples)
        persist_task = persist_result.s(sample.analysis_result.pk,
                                        MODULE_NAME)

        task_chain = chain(categories_task, distribution_task, persist_task)
        result = task_chain.delay()

        return result

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        categories_task = categories_from_metadata.s(samples, min_size=1)
        distribution_task = make_distributions.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)
        task_chain = chain(
            categories_task,
            distribution_task,
            persist_task,
        )
        result = task_chain.delay()

        return result
