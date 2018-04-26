"""Module for Beta Diversity results."""

from app.display_modules.display_module import DisplayModule
from app.tool_results.beta_diversity import BetaDiversityResultModule

from .constants import MODULE_NAME
from .models import BetaDiversityResult
from .wrangler import BetaDiversityWrangler


class BetaDiversityDisplayModule(DisplayModule):
    """Tasks for generating Beta Diversity results."""

    @staticmethod
    def required_tool_results():
        """Return a list of necessary tool results."""
        return [BetaDiversityResultModule]

    @classmethod
    def name(cls):
        """Return the name."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return embedded result."""
        return BetaDiversityResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler."""
        return BetaDiversityWrangler
