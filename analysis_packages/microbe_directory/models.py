"""Microbe Directory AnalysisModule models."""

import mongoengine as mdb


class MicrobeDirectoryResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Set of microbe directory results."""

    samples = mdb.DictField(required=True)
