"""Methyls module."""

from tool_packages.methyltransferases import MethylResultModule

from app.display_modules.display_module import SampleToolDisplayModule

from .constants import MODULE_NAME
from .models import MethylResult
from .wrangler import MethylWrangler


class MethylsDisplayModule(SampleToolDisplayModule):
    """Methyltransferase display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [MethylResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return MethylResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return MethylWrangler
