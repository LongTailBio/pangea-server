"""Tasks to process CARD results."""

from analysis_packages.generic_gene_set.analysis import filter_gene_results

from .constants import SOURCE_TOOL_NAME, TOP_N


def processor(*sample_data):
    """Wrap Beta Diversity component calculations."""
    samples = list(sample_data)
    return filter_gene_results(samples, SOURCE_TOOL_NAME, TOP_N)
