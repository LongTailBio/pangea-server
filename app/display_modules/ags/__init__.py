"""
Average Genome Size Module.

This plot display the distribution of average genome sizes
for different metadata attributes.
"""

from tool_packages.microbe_census import MicrobeCensusResultModule

from app.display_modules.display_module import SampleToolDisplayModule

# Re-export modules
from .ags_models import DistributionResult, AGSResult
from .ags_wrangler import AGSWrangler
from .constants import MODULE_NAME


class AGSDisplayModule(SampleToolDisplayModule):
    """AGS display module."""

    @classmethod
    def name(cls):
        """Return unique id string."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return data model for Sample Similarity type."""
        return AGSResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for Sample Similarity type."""
        return AGSWrangler

    @staticmethod
    def required_tool_results():
        """List requires ToolResult modules."""
        return [MicrobeCensusResultModule]
