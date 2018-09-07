"""Module for Beta Diversity results."""

from analysis_packages.base import GroupToolAnalysisModule
from tool_packages.beta_diversity import BetaDiversityResultModule

from .analysis import processor
from .constants import MODULE_NAME
from .models import BetaDiversityResult


class BetaDiversityAnalysisModule(GroupToolAnalysisModule):
    """Beta Diversity AnalysisModule."""

    @staticmethod
    def required_tool_results():
        """Return a list of necessary tool results."""
        return [BetaDiversityResultModule]

    @staticmethod
    def name():
        """Return the name."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return embedded result."""
        return BetaDiversityResult

    @staticmethod
    def processor():
        """Return function(group_tool_result) for proccessing sample data."""
        return processor
