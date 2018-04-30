"""
HMP Module.

This chart shows the average similarity between bacterial communities in the
samples and human body sites from the Human Microbiome Project.
"""

from app.display_modules.display_module import SampleToolDisplayModule
from app.tool_results.hmp_sites import HmpSitesResultModule

from .constants import MODULE_NAME
from .models import HMPResult
from .wrangler import HMPWrangler


class HMPDisplayModule(SampleToolDisplayModule):
    """HMP display module."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [HmpSitesResultModule]

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return data model for HMP type."""
        return HMPResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for HMP type."""
        return HMPWrangler
