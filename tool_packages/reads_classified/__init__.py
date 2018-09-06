"""Reads Classified tool module."""

from mongoengine import FloatField

from tool_packages.base import SampleToolResultModule
from tool_packages.base.models import ToolResult

from .constants import MODULE_NAME


class ReadsClassifiedToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Reads Classified tool's result type."""

    total = FloatField(required=True, default=0)
    viral = FloatField(required=True, default=0)
    archaeal = FloatField(required=True, default=0)
    bacterial = FloatField(required=True, default=0)
    host = FloatField(required=True, default=0)
    nonhost_macrobial = FloatField(required=True, default=0)
    fungal = FloatField(required=True, default=0)
    nonfungal_eukaryotic = FloatField(required=True, default=0)
    unknown = FloatField(required=True, default=0)


class ReadsClassifiedResultModule(SampleToolResultModule):
    """Reads Classified tool module."""

    @classmethod
    def name(cls):
        """Return Reads Classified module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Reads Classified module's model class."""
        return ReadsClassifiedToolResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, genes."""
        return [lambda payload: payload['proportions']]
