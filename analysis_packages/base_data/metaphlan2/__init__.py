"""Metaphlan 2 tool module."""

from analysis_packages.base import AnalysisModule

from .constants import MODULE_NAME
from .models import Metaphlan2Result


class Metaphlan2ResultModule(AnalysisModule):
    """Metaphlan 2 tool module."""

    @classmethod
    def name(cls):
        """Return Metaphlan 2 module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Metaphlan2 module's model class."""
        return Metaphlan2Result

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: {'taxa': payload}]
