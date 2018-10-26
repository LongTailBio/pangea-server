"""Methyltransferase tool module."""

from analysis_packages.base import AnalysisModule

from .constants import MODULE_NAME
from .models import MethylToolResult


class MethylResultModule(AnalysisModule):
    """Methyltransferase tool module."""

    @classmethod
    def name(cls):
        """Return Methyltransferase module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Methyltransferase module's model class."""
        return MethylToolResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: {'genes': payload}]
