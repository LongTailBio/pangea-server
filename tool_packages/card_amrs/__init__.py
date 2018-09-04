"""CARD AMR Alignment tool module."""

from tool_packages.base import SampleToolResultModule

from .constants import MODULE_NAME
from .models import CARDAMRToolResult


class CARDAMRResultModule(SampleToolResultModule):
    """CARD AMR Alignment tool module."""

    @classmethod
    def name(cls):
        """Return CARD AMR Alignment module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return CARD AMR Alignment module's model class."""
        return CARDAMRToolResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: {'genes': payload}]
