"""Virulence Factors display models."""

import mongoengine as mdb


class VFDBSampleDocument(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Tool document type."""

    rpkm = mdb.MapField(mdb.FloatField(), required=True)
    rpkmg = mdb.MapField(mdb.FloatField(), required=True)


class VFDBResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Sample Similarity document type."""

    sample_doc_field = mdb.EmbeddedDocumentField(VFDBSampleDocument)
    samples = mdb.MapField(field=sample_doc_field, required=True)
