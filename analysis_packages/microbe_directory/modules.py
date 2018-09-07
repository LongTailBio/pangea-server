"""Module for Microbe Directory results."""

from analysis_packages.base import SampleToolAnalysisModule
from tool_packages.microbe_directory import MicrobeDirectoryResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import MicrobeDirectoryResult


class MicrobeDirectoryAnalysisModule(SampleToolAnalysisModule):
    """Microbe Directory AnalysisModule."""

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return MicrobeDirectoryResult

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [MicrobeDirectoryResultModule]

    @staticmethod
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
