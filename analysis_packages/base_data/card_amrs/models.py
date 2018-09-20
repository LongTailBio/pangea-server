"""Models for Virulence Factor tool module."""

from mongoengine import EmbeddedDocument, MapField, EmbeddedDocumentField, FloatField

from analysis_packages.base.models import ModuleResult


class AMRRow(EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a gene in CARD AMR Alignment."""

    rpk = FloatField()
    rpkm = FloatField()
    rpkmg = FloatField()


class CARDAMRToolResult(ModuleResult):  # pylint: disable=too-few-public-methods
    """CARD AMR Alignment result type."""

    amr_row_field = EmbeddedDocumentField(AMRRow)
    genes = MapField(field=amr_row_field, required=True)

    @classmethod
    def vector_variables(cls):
        """Return the names of vector variables."""
        return ['genes']
