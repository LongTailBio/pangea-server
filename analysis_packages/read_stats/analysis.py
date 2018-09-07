"""Read Stats wrangler and related."""

from analysis_packages.base.utils import collate_samples
from analysis_packages.base.exceptions import UnsupportedAnalysisMode

from tool_packages.read_stats import ReadStatsToolResultModule


def processor(*samples):
    """Handle Read Stats component calculations."""
    samples = list(samples)
    if len(samples) < 2:
        raise UnsupportedAnalysisMode

    tool_name = ReadStatsToolResultModule.name()
    collate_fields = ReadStatsToolResultModule.result_model().stat_fields()
    collated_samples = collate_samples(tool_name, collate_fields, samples)
    return {'samples': collated_samples}
