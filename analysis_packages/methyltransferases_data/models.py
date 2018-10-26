"""Models for Methyltransferase tool module."""

from mongoengine import EmbeddedDocument, EmbeddedDocumentField, FloatField, MapField

from analysis_packages.base.models import ModuleResult


class MethylRow(EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in Methyltransferase."""

    rpk = FloatField()
    rpkm = FloatField()
    rpkmg = FloatField()


class MethylToolResult(ModuleResult):  # pylint: disable=too-few-public-methods
    """Methyltransferase result type."""

    genes = MapField(field=EmbeddedDocumentField(MethylRow),
                     required=True)
