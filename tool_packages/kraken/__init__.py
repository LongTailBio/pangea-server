"""Kraken tool module."""

from tool_packages.base import SampleToolResultModule

from .models import KrakenResult


MODULE_NAME = 'kraken_taxonomy_profiling'


class KrakenResultModule(SampleToolResultModule):
    """Kraken tool module."""

    @classmethod
    def name(cls):
        """Return Kraken module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Kraken module's model class."""
        return KrakenResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: {'taxa': payload}]
