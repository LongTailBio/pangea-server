"""Beta Diversity tool module."""

from tool_packages.base import GroupToolResultModule

from .models import BetaDiversityToolResult


MODULE_NAME = 'beta_diversity'


class BetaDiversityResultModule(GroupToolResultModule):
    """Beta Diversity tool module."""

    @classmethod
    def name(cls):
        """Return Beta Diversity module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Beta Diversity module's model class."""
        return BetaDiversityToolResult
