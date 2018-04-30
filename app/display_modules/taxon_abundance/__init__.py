"""
Taxon Abundance module.

This plot shows the relative abundance of each different microbes found in
each sample.

Hover over the plot to highlight connections. Thicker connections represent
larger proportions of taxa in a given sample.
"""

from app.display_modules.display_module import SampleToolDisplayModule

from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.krakenhll import KrakenHLLResultModule

from .constants import MODULE_NAME
from .models import TaxonAbundanceResult
from .wrangler import TaxonAbundanceWrangler


class TaxonAbundanceDisplayModule(SampleToolDisplayModule):
    """Taxon Abundance display module."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a taxon abundance sample must have."""
        taxa_modules = [
            Metaphlan2ResultModule,
            KrakenHLLResultModule,
            KrakenResultModule,
        ]
        return taxa_modules

    @classmethod
    def name(cls):
        """Return taxon abundance's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return status wrapper for Taxon Abundance type."""
        return TaxonAbundanceResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for Taxon Abundance type."""
        return TaxonAbundanceWrangler
