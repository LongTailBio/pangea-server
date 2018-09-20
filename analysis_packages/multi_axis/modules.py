"""Multi Axis module."""

from analysis_packages.base import AnalysisModule
from analysis_packages.base_data.card_amrs import CARDAMRResultModule
from analysis_packages.base_data.humann2_normalize import Humann2NormalizeResultModule
from analysis_packages.base_data.krakenhll import KrakenHLLResultModule
from analysis_packages.base_data.metaphlan2 import Metaphlan2ResultModule
from analysis_packages.base_data.microbe_census import MicrobeCensusResultModule


from .analysis import processor
from .constants import MODULE_NAME
from .models import MultiAxisResult


class MultiAxisAnalysisModule(AnalysisModule):
    """Multi Axis AnalysisModule."""

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return data model for Sample Similarity type."""
        return MultiAxisResult

    @staticmethod
    def required_modules():
        """Enumerate which ToolResult modules a sample must have."""
        return [
            KrakenHLLResultModule,
            Metaphlan2ResultModule,
            MicrobeCensusResultModule,
            CARDAMRResultModule,
            Humann2NormalizeResultModule
        ]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Multi-Axis sample data."""
        return processor
