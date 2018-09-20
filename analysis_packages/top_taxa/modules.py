"""Top Taxa AnalysisModule."""

from analysis_packages.base_data.krakenhll import KrakenHLLResultModule
from analysis_packages.base_data.metaphlan2 import Metaphlan2ResultModule

from analysis_packages.base import AnalysisModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import TopTaxaResult


class TopTaxaAnalysisModule(AnalysisModule):
    """TopTaxa AnalysisModule."""

    @staticmethod
    def name():
        """Return unique id string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return data model."""
        return TopTaxaResult

    @staticmethod
    def required_modules():
        """List requires ToolResult modules."""
        return [KrakenHLLResultModule, Metaphlan2ResultModule]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Top Taxa sample data."""
        return processor
