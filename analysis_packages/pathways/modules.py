"""Pathwaytransferase AnlysisModule."""

from analysis_packages.base import AnalysisModule
from tool_packages.humann2 import Humann2ResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import PathwayResult


class PathwaysAnalysisModule(AnalysisModule):
    """Pathwaytransferase AnalysisModule."""

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return PathwayResult

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [Humann2ResultModule]

    @staticmethod
    def single_sample_processor():
        """Return function(sample_data) for proccessing Pathways sample data."""
        return processor

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Pathways sample data."""
        return processor
