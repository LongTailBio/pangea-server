"""Module for alpha diversity results."""

from app.display_modules.display_module import SampleToolDisplayModule
from app.tool_results.alpha_diversity import AlphaDiversityResultModule

from .models import AlphaDiversityResult
from .wrangler import AlphaDivWrangler
from .constants import MODULE_NAME


class AlphaDivDisplayModule(SampleToolDisplayModule):
    """Alpha Diversity display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [AlphaDiversityResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return AlphaDiversityResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return AlphaDivWrangler
