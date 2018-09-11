"""Reads Classified Module."""

from analysis_packages.base import AnalysisModule
from tool_packages.reads_classified import ReadsClassifiedResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import ReadsClassifiedResult


class ReadsClassifiedAnalysisModule(AnalysisModule):
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
    def single_sample_processor():
        """Return function(sample_data) for proccessing Reads Classified sample data."""
        return processor

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Reads Classified sample data."""
        return processor
