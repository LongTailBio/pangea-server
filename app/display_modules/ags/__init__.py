"""
Average Genome Size Module.

This plot display the distribution of average genome sizes
for different metadata attributes.
"""

from app.display_modules.display_module import SampleToolDisplayModule
from app.tool_results.microbe_census import MicrobeCensusResultModule

# Re-export modules
from .ags_models import DistributionResult, AGSResult
from .ags_wrangler import AGSWrangler


class AGSDisplayModule(SampleToolDisplayModule):
    """AGS display module."""

    @classmethod
    def name(cls):
        """Return unique id string."""
        return 'average_genome_size'

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
