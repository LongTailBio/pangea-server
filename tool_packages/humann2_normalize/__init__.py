"""Humann2 Normalize tool module."""

from tool_packages.base import SampleToolResultModule

from .constants import MODULE_NAME
from .models import Humann2NormalizeToolResult


class Humann2NormalizeResultModule(SampleToolResultModule):
    """Humann2 Normalize tool module."""

    @classmethod
    def name(cls):
        """Return Humann2 Normalize module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Humann2 Normalize module's model class."""
        return Humann2NormalizeToolResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: {'genes': payload}]
