"""Volcano plot module."""

from analysis_packages.base import SampleToolAnalysisModule
from tool_packages.kraken import KrakenResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import VolcanoResult


class VolcanoAnalysisModule(SampleToolAnalysisModule):
    """Volcano AnalysisModule."""

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return data model for Sample Similarity type."""
        return VolcanoResult

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [
            KrakenResultModule,
            Metaphlan2ResultModule,
        ]

    @staticmethod
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
