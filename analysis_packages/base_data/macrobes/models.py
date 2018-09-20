"""Models for Macrobial tool module."""

from mongoengine import EmbeddedDocument, EmbeddedDocumentField, MapField, IntField, FloatField

from analysis_packages.base.models import ModuleResult


class MacrobialRow(EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in Macrobial."""

    total_reads = IntField()
    rpkm = FloatField()


class MacrobeToolResult(ModuleResult):  # pylint: disable=too-few-public-methods
    """Macrobial result type."""

    macrobe_row_field = EmbeddedDocumentField(MacrobialRow)
    macrobes = MapField(field=macrobe_row_field, required=True)
