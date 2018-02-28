"""Shortbred tool module."""

from app.extensions import mongoDB
from app.tool_results.tool_module import ToolResult, ToolResultModule


class ShortbredResult(ToolResult):
    """Shortbred tool's result type."""

    abundances = mongoDB.DictField()


class ShortbredResultModule(ToolResultModule):
    """Shortbred tool module."""

    @classmethod
    def name(cls):
        """Return Shortbred module's unique identifier string."""
        return 'shortbred'
