"""Taxon Abundance module."""

from analysis_packages.base import SampleToolAnalysisModule
from tool_packages.kraken import KrakenResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule
from tool_packages.krakenhll import KrakenHLLResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import TaxonAbundanceResult


class TaxonAbundanceAnalysisModule(SampleToolAnalysisModule):
    """Taxon Abundance AnalysisModule."""

    @staticmethod
    def name():
        """Return taxon abundance's unique identifier string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return status wrapper for Taxon Abundance type."""
        return TaxonAbundanceResult

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a taxon abundance sample must have."""
        taxa_modules = [
            Metaphlan2ResultModule,
            KrakenHLLResultModule,
            KrakenResultModule,
        ]
        return taxa_modules

    @staticmethod
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
