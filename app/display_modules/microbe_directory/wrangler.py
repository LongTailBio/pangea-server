"""Wrangler for Microbe Directory results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler

from .constants import MODULE_NAME
from .tasks import (
    microbe_directory_reducer,
    persist_result,
    collate_microbe_directory
)


class MicrobeDirectoryWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather single sample and process."""
        samples = [sample]
        collate_task = collate_microbe_directory.s(samples)
        reducer_task = microbe_directory_reducer.s()
        analysis_result_uuid = sample['analysis_result']
        persist_task = persist_result.s(analysis_result_uuid, MODULE_NAME)

        task_chain = chain(collate_task, reducer_task, persist_task)
        result = task_chain.delay()

        return result

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        collate_task = collate_microbe_directory.s(samples)
        reducer_task = microbe_directory_reducer.s()
        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)

        task_chain = chain(collate_task, reducer_task, persist_task)
        result = task_chain.delay()

        return result
