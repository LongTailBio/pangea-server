"""Factory for generating KrakenHLL result models for testing."""

from tool_packages.kraken.tests.factory import create_values

from app.tool_results.krakenhll import KrakenHLLResult


def create_krakenhll(taxa_count=10):
    """Create KrakenHLL Result with specified number of taxa."""
    taxa = create_values(taxa_count=taxa_count)
    return KrakenHLLResult(taxa=taxa).save()
