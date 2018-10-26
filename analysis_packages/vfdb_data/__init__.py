"""Virulence Factor tool module."""

from analysis_packages.base import AnalysisModule

from .constants import MODULE_NAME
from .models import VFDBToolResult


class VFDBResultModule(AnalysisModule):
    """Virulence Factor tool module."""

    @classmethod
    def name(cls):
        """Return Virulence Factor module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Virulence Factor module's model class."""
        return VFDBToolResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: {'genes': payload}]
