"""Models for Humann2 Normalize tool module."""

from mongoengine import EmbeddedDocument, EmbeddedDocumentField, MapField, FloatField

from analysis_packages.base.models import ModuleResult


class Humann2NormalizeRow(EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in Humann2 Normalize."""

    rpk = FloatField()
    rpkm = FloatField()
    rpkmg = FloatField()


class Humann2NormalizeToolResult(ModuleResult):  # pylint: disable=too-few-public-methods
    """Humann2 Normalize result type."""

    hum_row_field = EmbeddedDocumentField(Humann2NormalizeRow)
    genes = MapField(field=hum_row_field, required=True)

    @classmethod
    def vector_variables(cls):
        """Return the names of vector variables."""
        return ['genes']
