"""Tasks for generating Multi Axis results."""

from celery import chord

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import categories_from_metadata

from .constants import MODULE_NAME
from .tasks import make_axes, persist_result, multi_axis_reducer


class MultiAxisWrangler(DisplayModuleWrangler):
    """Task for generating Multi Axis results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather samples and process."""
        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)

        categories_task = categories_from_metadata.s(samples)
        make_axes_task = make_axes.s(samples)

        return chord([make_axes_task, categories_task])(multi_axis_reducer | persist_task)
