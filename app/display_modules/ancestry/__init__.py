"""Module for Ancestry results."""

from tool_packages.ancestry import AncestryResultModule

from app.display_modules.display_module import SampleToolDisplayModule

from .constants import MODULE_NAME
from .models import AncestryResult
from .wrangler import AncestryWrangler


class AncestryDisplayModule(SampleToolDisplayModule):
    """Ancestry display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [AncestryResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return AncestryResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return AncestryWrangler
