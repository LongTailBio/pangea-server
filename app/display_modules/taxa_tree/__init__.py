"""Taxon Tree display module."""

from tool_packages.kraken import KrakenResultModule

from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.display_modules.display_module import SampleToolDisplayModule

from .constants import MODULE_NAME
from .models import TaxaTreeResult
from .wrangler import TaxaTreeWrangler


class TaxaTreeDisplayModule(SampleToolDisplayModule):
    """Read Stats display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules for taxa tree."""
        return [Metaphlan2ResultModule, KrakenResultModule, KrakenHLLResultModule]

    @classmethod
    def name(cls):
        """Return the name of the taxa tree module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return TaxaTreeResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return TaxaTreeWrangler
