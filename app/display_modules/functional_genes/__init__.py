"""Virulence Factor module."""

from tool_packages.humann2_normalize import Humann2NormalizeResultModule

from app.display_modules.display_module import SampleToolDisplayModule

from .models import FunctionalGenesSampleDocument, FunctionalGenesResult
from .wrangler import FunctionalGenesWrangler
from .constants import MODULE_NAME


class FunctionalGenesDisplayModule(SampleToolDisplayModule):
    """Virulence factors display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [Humann2NormalizeResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return FunctionalGenesResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return FunctionalGenesWrangler
