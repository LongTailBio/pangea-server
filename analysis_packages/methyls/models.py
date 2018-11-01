"""Methyls display models."""

import mongoengine as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name


class MethylSampleDocument(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Methyl document type."""

    rpkm = mdb.MapField(mdb.FloatField(), required=True)
    rpkmg = mdb.MapField(mdb.FloatField(), required=True)


class MethylResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Methyls document type."""

    samples = mdb.MapField(field=EmbeddedDoc(MethylSampleDocument), required=True)
