"""Kraken tool module."""

from analysis_packages.base import AnalysisModule

from .constants import MODULE_NAME
from .models import KrakenHLLResult


class KrakenHLLResultModule(AnalysisModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return Kraken module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Kraken module's model class."""
        return KrakenHLLResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, taxa."""
        return [lambda payload: {'taxa': payload}]
