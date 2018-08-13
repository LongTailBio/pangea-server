"""Models for Humann2 Normalize tool module."""

from app.extensions import mongoDB
from app.tool_results.models import ToolResult


class Humann2NormalizeRow(mongoDB.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in Humann2 Normalize."""

    rpk = mongoDB.FloatField()
    rpkm = mongoDB.FloatField()
    rpkmg = mongoDB.FloatField()


class Humann2NormalizeToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Humann2 Normalize result type."""

    hum_row_field = mongoDB.EmbeddedDocumentField(Humann2NormalizeRow)
    genes = mongoDB.MapField(field=hum_row_field, required=True)

    @classmethod
    def vector_variables(cls):
        """Return the names of vector variables."""
        return ['genes']
