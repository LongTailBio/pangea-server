"""Read Stats AnalysisModule."""

from analysis_packages.base import AnalysisModule
from analysis_packages.base_data.read_stats import ReadStatsToolResultModule

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
    def required_modules():
        """Return a list of the necessary result modules."""
        return [ReadStatsToolResultModule]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Read Stats sample data."""
        return processor
