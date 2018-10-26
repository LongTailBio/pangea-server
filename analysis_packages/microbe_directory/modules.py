"""Module for Microbe Directory results."""

from analysis_packages.base import AnalysisModule
from analysis_packages.microbe_directory_data import MicrobeDirectoryResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import MicrobeDirectoryResult


class MicrobeDirectoryAnalysisModule(AnalysisModule):
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
    def required_modules():
        """Return a list of the necessary result modules."""
        return [MicrobeDirectoryResultModule]

    @staticmethod
    def single_sample_processor():
        """Return function(sample_data) for proccessing Microbe sample data."""
        return processor

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Microbe sample data."""
        return processor
