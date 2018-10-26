"""Alpha Diversity AnalysisModule."""

from analysis_packages.base import AnalysisModule
from analysis_packages.alpha_diversity_data import AlphaDiversityToolResult

from .analysis import processor
from .models import AlphaDiversityResult
from .constants import MODULE_NAME


class AlphaDivAnalysisModule(AnalysisModule):
    """Alpha Diversity AnalysisModule."""

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return AlphaDiversityResult

    @staticmethod
    def required_modules():
        """Return a list of the necessary result modules."""
        return [AlphaDiversityToolResult]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Alpha Diversity sample data."""
        return processor
