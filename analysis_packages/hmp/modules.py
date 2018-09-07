"""HMP Module."""

from analysis_packages.base import SampleToolAnalysisModule
from tool_packages.hmp_sites import HmpSitesResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import HMPResult


class HMPAnalysisModule(SampleToolAnalysisModule):
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
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
