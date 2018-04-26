"""Wrangler for alpha diversity display module."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import categories_from_metadata

from .constants import MODULE_NAME
from .tasks import make_alpha_distributions, persist_result


class AlphaDivWrangler(DisplayModuleWrangler):
    """Tasks for generating alpha div results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process Alpha Diversity for samples."""
        categories_task = categories_from_metadata.s(samples, min_size=1)
        distribution_task = make_alpha_distributions.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid,
                                        MODULE_NAME)
        task_chain = chain(categories_task, distribution_task, persist_task)
        result = task_chain.delay()

        return result
