"""Factory for generating KrakenHLL result models for testing."""

from app.tool_results.krakenhll import KrakenHLLResult
from app.tool_results.kraken.tests.factory import create_taxa


def create_krakenhll(taxa_count=10):
    """Create KrakenResult with specified number of taxa."""
    taxa = create_taxa(taxa_count)
    return KrakenHLLResult(taxa=taxa).save()
