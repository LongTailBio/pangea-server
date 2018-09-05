"""Factory for generating Metaphlan2 result models for testing."""

from tool_packages.kraken.tests.factory import create_values

from ..models import Metaphlan2Result


def create_result(taxa_count=10, save=True):
    """Create Metaphlan2Result with specified number of taxa."""
    taxa = create_values(taxa_count=taxa_count)
    result = Metaphlan2Result(taxa=taxa)
    if save:
        result.save()
    return result
