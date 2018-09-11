"""HMP Module."""

from analysis_packages.base import AnalysisModule
from tool_packages.hmp_sites import HmpSitesResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import HMPResult


class HMPAnalysisModule(AnalysisModule):
    """HMP AnalysisModule."""

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return data model for HMP type."""
        return HMPResult

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [HmpSitesResultModule]

    @staticmethod
    def single_sample_processor():
        """Return function(sample_data) for proccessing HMP sample data."""
        return processor

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing HMP sample data."""
        return processor
