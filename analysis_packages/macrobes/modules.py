"""Module for Macrobe results."""

from analysis_packages.base import SampleToolAnalysisModule
from tool_packages.macrobes import MacrobeResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import MacrobeResult


class MacrobeAnalysisModule(SampleToolAnalysisModule):
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
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [MacrobeResultModule]

    @staticmethod
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
