"""Alpha Diversity AnalysisModule."""

from analysis_packages.base import AnalysisModule
from tool_packages.alpha_diversity import AlphaDiversityResultModule

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
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [AlphaDiversityResultModule]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Alpha Diversity sample data."""
        return processor
