"""Reads Classified Module."""

from analysis_packages.base import SampleToolAnalysisModule
from tool_packages.reads_classified import ReadsClassifiedResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import ReadsClassifiedResult


class ReadsClassifiedAnalysisModule(SampleToolAnalysisModule):
    """Reads Classified AnalysisModule."""

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return data model for Reads Classified type."""
        return ReadsClassifiedResult

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [ReadsClassifiedResultModule]

    @staticmethod
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
