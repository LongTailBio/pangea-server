"""Top Taxa AnalysisModule."""

from tool_packages.krakenhll import KrakenHLLResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule

from analysis_packages.base import SampleToolAnalysisModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import TopTaxaResult


class TopTaxaAnalysisModule(SampleToolAnalysisModule):
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
    def required_tool_results():
        """List requires ToolResult modules."""
        return [KrakenHLLResultModule, Metaphlan2ResultModule]

    @staticmethod
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
