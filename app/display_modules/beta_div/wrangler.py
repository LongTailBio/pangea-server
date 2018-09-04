"""Wrangler for Beta Diversity display module."""

from tool_packages.beta_diversity.models import BetaDiversityToolResult

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import jsonify

from .constants import MODULE_NAME
from .tasks import persist_result


class BetaDiversityWrangler(DisplayModuleWrangler):
    """Tasks for generating beta diversity results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Process a beta diversity result."""
        analysis_result_uuid = sample_group.analysis_result_uuid
        tool_result = BetaDiversityToolResult.objects.get(sample_group_uuid=sample_group.id)
        result_data = {'data': jsonify(tool_result)['data']}
        persist_task = persist_result.s(result_data, analysis_result_uuid, MODULE_NAME)

        result = persist_task.delay()
        return result
