"""Sample Similarity module."""

from analysis_packages.base import AnalysisModule
from tool_packages.kraken import KrakenResultModule
from tool_packages.krakenhll import KrakenHLLResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import SampleSimilarityResult


class SampleSimilarityAnalysisModule(AnalysisModule):
    """Sample Similarity AnalysisModule."""

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return data model for Sample Similarity type."""
        return SampleSimilarityResult

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [KrakenResultModule, KrakenHLLResultModule, Metaphlan2ResultModule]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Sample Similarity sample data."""
        return processor
