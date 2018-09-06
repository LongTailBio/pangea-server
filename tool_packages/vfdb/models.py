"""Models for Virulence Factor tool module."""

from mongoengine import EmbeddedDocument, EmbeddedDocumentField, FloatField, MapField

from tool_packages.base.models import ToolResult


class VFDBRow(EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in VFDB."""

    rpk = FloatField()
    rpkm = FloatField()
    rpkmg = FloatField()


class VFDBToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Virulence Factor result type."""

    vfdb_row_field = EmbeddedDocumentField(VFDBRow)
    genes = MapField(field=vfdb_row_field, required=True)
