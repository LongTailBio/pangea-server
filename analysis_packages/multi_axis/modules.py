"""Multi Axis module."""

from analysis_packages.base import AnalysisModule
from tool_packages.card_amrs import CARDAMRResultModule
from tool_packages.humann2_normalize import Humann2NormalizeResultModule
from tool_packages.krakenhll import KrakenHLLResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule
from tool_packages.microbe_census import MicrobeCensusResultModule


from .analysis import processor
from .constants import MODULE_NAME
from .models import MultiAxisResult


class MultiAxisAnalysisModule(AnalysisModule):
    """Multi Axis AnalysisModule."""

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return data model for Sample Similarity type."""
        return MultiAxisResult

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [
            KrakenHLLResultModule,
            Metaphlan2ResultModule,
            MicrobeCensusResultModule,
            CARDAMRResultModule,
            Humann2NormalizeResultModule
        ]

    @staticmethod
    def sample_processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
