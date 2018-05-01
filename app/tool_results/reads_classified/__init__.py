"""Reads Classified tool module."""

from app.extensions import mongoDB
from app.tool_results.modules import SampleToolResultModule
from app.tool_results.models import ToolResult

from .constants import MODULE_NAME


class ReadsClassifiedToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Reads Classified tool's result type."""

    total = mongoDB.FloatField(required=True, default=0)
    viral = mongoDB.FloatField(required=True, default=0)
    archaeal = mongoDB.FloatField(required=True, default=0)
    bacterial = mongoDB.FloatField(required=True, default=0)
    host = mongoDB.FloatField(required=True, default=0)
    nonhost_macrobial = mongoDB.FloatField(required=True, default=0)
    fungal = mongoDB.FloatField(required=True, default=0)
    nonfungal_eukaryotic = mongoDB.FloatField(required=True, default=0)
    unknown = mongoDB.FloatField(required=True, default=0)


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
