"""Macrobe tool module."""

from tool_packages.base import SampleToolResultModule

from .constants import MODULE_NAME
from .models import MacrobeToolResult


class MacrobeResultModule(SampleToolResultModule):
    """Macrobe tool module."""

    @classmethod
    def name(cls):
        """Return Macrobe module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Macrobe module's model class."""
        return MacrobeToolResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, macrobes."""
        return [lambda payload: {'macrobes': payload}]
