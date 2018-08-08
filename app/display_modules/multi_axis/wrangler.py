"""Tasks for generating Multi Axis results."""

from celery import chord

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import categories_from_metadata

from .tasks import make_axes, persist_result, multi_axis_reducer


class MultiAxisWrangler(DisplayModuleWrangler):
    """Task for generating Multi Axis results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather samples and process."""
        reducer_task = multi_axis_reducer.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid)

        middle_tasks = [
            make_axes.s(samples),
            categories_from_metadata.s(samples),
        ]

        return chord(middle_tasks)(reducer_task | persist_task)
