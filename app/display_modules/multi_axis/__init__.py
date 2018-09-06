"""
Multi Axis module.

This plot displays various dimensionality reductions.

The user is given a choice of a large number of axes which can
be plotted together as a scatter plot.
"""

from tool_packages.card_amrs import CARDAMRResultModule
from tool_packages.humann2_normalize import Humann2NormalizeResultModule
from tool_packages.krakenhll import KrakenHLLResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule
from tool_packages.microbe_census import MicrobeCensusResultModule

from app.display_modules.display_module import SampleToolDisplayModule

# Re-export modules
from .constants import MODULE_NAME
from .models import MultiAxisResult, AxisDocument
from .wrangler import MultiAxisWrangler


class MultiAxisDisplayModule(SampleToolDisplayModule):
    """Multi Axis display module."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [
            KrakenHLLResultModule,
            Metaphlan2ResultModule,
            MicrobeCensusResultModule,
            CARDAMRResultModule,
            Humann2NormalizeResultModule
        ]

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return data model for Sample Similarity type."""
        return MultiAxisResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for Sample Similarity type."""
        return MultiAxisWrangler
