"""Read Stats AnalysisModule."""

from analysis_packages.base import AnalysisModule
from tool_packages.read_stats import ReadStatsToolResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import ReadStatsResult


class ReadStatsAnalysisModule(AnalysisModule):
    """Read Stats AnalysisModule."""

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return ReadStatsResult

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [ReadStatsToolResultModule]

    @staticmethod
    def sample_processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
