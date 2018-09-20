"""Alpha Diversity tool module."""

from analysis_packages.base import AnalysisModule

from .models import AlphaDiversityToolResult


class AlphaDiversityBaseData(AnalysisModule):
    """Alpha Diversity tool module."""

    @classmethod
    def name(cls):
        """Return Alpha Diversity module's unique identifier string."""
        return 'alpha_diversity_stats'

    @classmethod
    def result_model(cls):
        """Return Alpha Diversity module's model class."""
        return AlphaDiversityToolResult
