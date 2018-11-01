"""Virulence Factors display models."""

import mongoengine as mdb


class FunctionalGenesSampleDocument(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Row in Functional Genes table document type."""

    rpkm = mdb.MapField(mdb.FloatField(), required=True)
    rpkmg = mdb.MapField(mdb.FloatField(), required=True)


class FunctionalGenesResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Fucntioanl Genes document type."""

    samples = mdb.MapField(field=mdb.EmbeddedDocumentField(FunctionalGenesSampleDocument),
                           required=True)
