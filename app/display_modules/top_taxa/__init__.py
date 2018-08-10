"""
Top Taxa Display Module.

Show the top taxa across different metadata groups and kingdoms.
"""

from app.display_modules.display_module import SampleToolDisplayModule
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule

# Re-export modules
from .models import TopTaxaResult
from .wrangler import TopTaxaWrangler
from .constants import MODULE_NAME


class TopTaxaDisplayModule(SampleToolDisplayModule):
    """TopTaxa display module."""

    @classmethod
    def name(cls):
        """Return unique id string."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return data model."""
        return TopTaxaResult

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler."""
        return TopTaxaWrangler

    @staticmethod
    def required_tool_results():
        """List requires ToolResult modules."""
        return [KrakenHLLResultModule, Metaphlan2ResultModule]
