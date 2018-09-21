"""Read Stats wrangler and related."""

from analysis_packages.base.utils import collate_samples

from analysis_packages.base_data.read_stats import ReadStatsToolResultModule


def processor(*samples):
    """Handle Read Stats component calculations."""
    tool_name = ReadStatsToolResultModule.name()
    collate_fields = ReadStatsToolResultModule.result_model().stat_fields()
    collated_samples = collate_samples(tool_name, collate_fields, samples)
    return {'samples': collated_samples}
