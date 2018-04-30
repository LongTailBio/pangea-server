"""Reads Classified display models."""

from app.extensions import mongoDB as mdb


class SingleReadsClassifiedResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Reads Classified for one sample."""

    total = mdb.IntField(required=True, default=0)
    viral = mdb.IntField(required=True, default=0)
    archaeal = mdb.IntField(required=True, default=0)
    bacterial = mdb.IntField(required=True, default=0)
    host = mdb.IntField(required=True, default=0)
    nonhost_macrobial = mdb.IntField(required=True, default=0)
    fungal = mdb.IntField(required=True, default=0)
    nonfungal_eukaryotic = mdb.IntField(required=True, default=0)
    unknown = mdb.IntField(required=True, default=0)


class ReadsClassifiedResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Read stats embedded result."""

    samples = mdb.MapField(field=mdb.EmbeddedDocumentField(SingleReadsClassifiedResult),
                           required=True)
