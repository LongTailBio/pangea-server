"""Read Stats wrangler and related."""

from celery import chain

from tool_packages.read_stats import ReadStatsToolResultModule

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import collate_samples

from .constants import MODULE_NAME
from .tasks import read_stats_reducer, persist_result


class ReadStatsWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        analysis_group_uuid = sample_group.analysis_result_uuid

        collate_task = collate_samples.s(
            ReadStatsToolResultModule.name(),
            ReadStatsToolResultModule.result_model().stat_fields(),
            samples
        )
        persist_task = persist_result.s(analysis_group_uuid, MODULE_NAME)

        task_chain = chain(collate_task,
                           read_stats_reducer.s(),
                           persist_task)
        result = task_chain.delay()

        return result
