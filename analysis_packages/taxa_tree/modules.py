"""Taxon Tree AnalysisModule."""

from analysis_packages.base import AnalysisModule
from analysis_packages.base_data.kraken import KrakenResultModule
from analysis_packages.base_data.krakenhll import KrakenHLLResultModule
from analysis_packages.base_data.metaphlan2 import Metaphlan2ResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import TaxaTreeResult


class TaxaTreeAnalysisModule(AnalysisModule):
    """Read Stats AnalysisModule."""

    @staticmethod
    def name():
        """Return the name of the taxa tree module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return TaxaTreeResult

    @staticmethod
    def required_modules():
        """Return a list of the necessary result modules for taxa tree."""
        return [Metaphlan2ResultModule, KrakenResultModule, KrakenHLLResultModule]

    @staticmethod
    def single_sample_processor():
        """Return function(sample_data) for proccessing Taxon Tree sample data."""
        return processor
