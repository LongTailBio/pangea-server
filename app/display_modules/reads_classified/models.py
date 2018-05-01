"""Reads Classified display models."""

from app.extensions import mongoDB as mdb


class SingleReadsClassifiedResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Reads Classified for one sample."""

    viral = mdb.FloatField(required=True, default=0)
    archaeal = mdb.FloatField(required=True, default=0)
    bacterial = mdb.FloatField(required=True, default=0)
    host = mdb.FloatField(required=True, default=0)
    nonhost_macrobial = mdb.FloatField(required=True, default=0)
    fungal = mdb.FloatField(required=True, default=0)
    nonfungal_eukaryotic = mdb.FloatField(required=True, default=0)
    unknown = mdb.FloatField(required=True, default=0)


class ReadsClassifiedResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Read stats embedded result."""

    samples = mdb.MapField(field=mdb.EmbeddedDocumentField(SingleReadsClassifiedResult),
                           required=True)
