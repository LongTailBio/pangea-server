"""Module for Microbe Directory results."""

from app.tool_results.microbe_directory import MicrobeDirectoryResultModule
from app.display_modules.display_module import SampleToolDisplayModule

from .constants import MODULE_NAME
from .models import MicrobeDirectoryResult
from .wrangler import MicrobeDirectoryWrangler


class MicrobeDirectoryDisplayModule(SampleToolDisplayModule):
    """Microbe Directory display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [MicrobeDirectoryResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return MicrobeDirectoryResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return MicrobeDirectoryWrangler
