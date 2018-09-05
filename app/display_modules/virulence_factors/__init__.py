"""Virulence Factor module."""

from tool_packages.vfdb import VFDBResultModule

from app.display_modules.display_module import SampleToolDisplayModule

from .models import VFDBSampleDocument, VFDBResult
from .wrangler import VFDBWrangler
from .constants import MODULE_NAME


class VirulenceFactorsDisplayModule(SampleToolDisplayModule):
    """Virulence factors display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [VFDBResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return VFDBResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return VFDBWrangler
