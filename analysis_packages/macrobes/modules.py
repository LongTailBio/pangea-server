"""Module for Macrobe results."""

from analysis_packages.base import AnalysisModule
from analysis_packages.macrobes_data import MacrobeResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import MacrobeResult


class MacrobeAnalysisModule(AnalysisModule):
    """Microbe Directory display module."""

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return MacrobeResult

    @staticmethod
    def required_modules():
        """Return a list of the necessary result modules."""
        return [MacrobeResultModule]

    @staticmethod
    def single_sample_processor():
        """Return function(sample_data) for proccessing Macrobe sample data."""
        return processor

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Macrobe sample data."""
        return processor
