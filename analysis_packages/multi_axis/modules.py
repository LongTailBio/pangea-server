"""Multi Axis module."""

from analysis_packages.base import AnalysisModule
from analysis_packages.card_amrs_data import CARDAMRResultModule
from analysis_packages.humann2_normalize_data import Humann2NormalizeResultModule
from analysis_packages.krakenhll_data import KrakenHLLResultModule
from analysis_packages.metaphlan2_data import Metaphlan2ResultModule
from analysis_packages.microbe_census_data import MicrobeCensusResultModule


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
