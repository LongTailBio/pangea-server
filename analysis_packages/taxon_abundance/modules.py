"""Taxon Abundance module."""

from analysis_packages.base import AnalysisModule
from analysis_packages.base_data.kraken import KrakenResultModule
from analysis_packages.base_data.metaphlan2 import Metaphlan2ResultModule
from analysis_packages.base_data.krakenhll import KrakenHLLResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import TaxonAbundanceResult


class TaxonAbundanceAnalysisModule(AnalysisModule):
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
    def required_modules():
        """Enumerate which ToolResult modules a taxon abundance sample must have."""
        taxa_modules = [
            Metaphlan2ResultModule,
            KrakenHLLResultModule,
            KrakenResultModule,
        ]
        return taxa_modules

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Taxon Abundance sample data."""
        return processor
