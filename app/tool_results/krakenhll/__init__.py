"""Kraken tool module."""

from app.tool_results.modules import SampleToolResultModule

from .models import KrakenHLLResult


class KrakenHLLResultModule(SampleToolResultModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return Kraken module's unique identifier string."""
        return 'krakenhll_taxonomy_profiling'

    @classmethod
    def result_model(cls):
        """Return Kraken module's model class."""
        return KrakenHLLResult
