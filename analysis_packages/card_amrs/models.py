"""Virulence Factors display models."""

import mongoengine as mdb


class CARDGenesSampleDocument(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Tool document type."""

    rpkm = mdb.MapField(mdb.FloatField(), required=True)
    rpkmg = mdb.MapField(mdb.FloatField(), required=True)


class CARDGenesResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Sample Similarity document type."""

    samples = mdb.MapField(field=mdb.EmbeddedDocumentField(CARDGenesSampleDocument),
                           required=True)
