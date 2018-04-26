"""Alpha Diversity tool module."""

from app.tool_results.modules import SampleToolResultModule

from .models import AlphaDiversityToolResult


class AlphaDiversityResultModule(SampleToolResultModule):
    """Alpha Diversity tool module."""

    @classmethod
    def name(cls):
        """Return Alpha Diversity module's unique identifier string."""
        return 'alpha_diversity_stats'

    @classmethod
    def result_model(cls):
        """Return Alpha Diversity module's model class."""
        return AlphaDiversityToolResult
