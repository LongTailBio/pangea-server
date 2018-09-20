"""Volcano plot module."""

from analysis_packages.base import AnalysisModule
from analysis_packages.base_data.kraken import KrakenResultModule
from analysis_packages.base_data.metaphlan2 import Metaphlan2ResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import VolcanoResult


class VolcanoAnalysisModule(AnalysisModule):
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
    def required_modules():
        """Enumerate which ToolResult modules a sample must have."""
        return [
            KrakenResultModule,
            Metaphlan2ResultModule,
        ]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Volcano sample data."""
        return processor
