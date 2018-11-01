"""Read Stats display models."""

import mongoengine as mdb


class ReadStatsSample(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """A set of consistent fields for read stats."""

    num_reads = mdb.IntField()
    gc_content = mdb.FloatField()
    codons = mdb.MapField(field=mdb.IntField(), required=True)
    tetramers = mdb.MapField(field=mdb.IntField(), required=True)


class ReadStatsResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Read stats embedded result."""

    samples = mdb.MapField(field=mdb.EmbeddedDocumentField(ReadStatsSample),
                           required=True)
