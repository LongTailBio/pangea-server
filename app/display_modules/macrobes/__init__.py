"""Module for Macrobe results."""

from app.tool_results.macrobes import MacrobeResultModule
from app.display_modules.display_module import DisplayModule

from .constants import MODULE_NAME
from .models import MacrobeResult
from .wrangler import MacrobeWrangler


class MacrobeDisplayModule(DisplayModule):
    """Microbe Directory display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [MacrobeResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return MacrobeResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return MacrobeWrangler
