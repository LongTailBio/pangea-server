"""Macrobe AnalysisModule models."""

import mongoengine as mdb


class MacrobeResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Set of macrobe results."""

    samples = mdb.MapField(mdb.MapField(mdb.FloatField()), required=True)
