"""
Reads Classified Module.

This chart shows the proportion of reads in each sample assigned to different groups.
"""

from tool_packages.reads_classified import ReadsClassifiedResultModule

from app.display_modules.display_module import SampleToolDisplayModule

# Re-export modules
from .models import ReadsClassifiedResult, SingleReadsClassifiedResult
from .wrangler import ReadsClassifiedWrangler
from .constants import MODULE_NAME


class ReadsClassifiedModule(SampleToolDisplayModule):
    """Reads Classified display module."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [ReadsClassifiedResultModule]

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return data model for Reads Classified type."""
        return ReadsClassifiedResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for Reads Classified type."""
        return ReadsClassifiedWrangler
