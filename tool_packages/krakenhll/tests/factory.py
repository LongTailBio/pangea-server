"""Factory for generating KrakenHLL result models for testing."""

from tool_packages.kraken.tests.factory import create_values

from ..models import KrakenHLLResult


def create_result(taxa_count=10, save=True):
    """Create KrakenHLL Result with specified number of taxa."""
    taxa = create_values(taxa_count=taxa_count)
    result = KrakenHLLResult(taxa=taxa)
    if save:
        result.save()
    return result
