"""Module for Ancestry results."""

from analysis_packages.base import AnalysisModule
from tool_packages.ancestry import AncestryResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import AncestryResult


class AncestryAnalysisModule(AnalysisModule):
    """Ancestry display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [AncestryResultModule]

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return AncestryResult

    @staticmethod
    def single_sample_processor():
        """Return function(sample_data) for proccessing Ancestry sample data."""
        return processor

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Ancestry sample data."""
        return processor
