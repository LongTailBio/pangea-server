"""Pathwaytransferase display module."""

from app.display_modules.display_module import DisplayModule
from app.tool_results.humann2 import Humann2ResultModule

from .constants import MODULE_NAME
from .models import PathwayResult
from .wrangler import PathwayWrangler


class PathwaysDisplayModule(DisplayModule):
    """Pathwaytransferase display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [Humann2ResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return PathwayResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return PathwayWrangler
