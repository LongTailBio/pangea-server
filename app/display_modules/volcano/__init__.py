"""Volcano plot module.

This module shows what features differ between a
particular metadata category and the rest of this group.

These differences proceed on two axes, the mean log fold change
between the selected category and the background, and the
negative log of the p-value of the difference.

Since p-value is partly based on the magnitude of the difference
this creates a plot that looks vaguely like a volcano exploding.
Points on the top right and left are likely to be both signfiicant
and testable.
"""


from app.display_modules.display_module import DisplayModule
from app.display_modules.sample_similarity.constants import MODULE_NAME
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule

# Re-export modules
from .constants import MODULE_NAME
from .models import VolcanoResult
from .wrangler import VolcanoWrangler


class VolcanoDisplayModule(DisplayModule):
    """Sample Similarity display module."""

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have."""
        return [
            KrakenResultModule,
            Metaphlan2ResultModule,
        ]

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return data model for Sample Similarity type."""
        return VolcanoResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for Sample Similarity type."""
        return VolcanoWrangler
