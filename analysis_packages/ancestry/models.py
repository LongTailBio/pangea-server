# pylint: disable=too-few-public-methods

"""Microbe Directory display models."""

import mongoengine as mdb


# Define alias
EmDoc = mdb.EmbeddedDocumentField  # pylint: disable=invalid-name


class PopulationEntry(mdb.EmbeddedDocument):
    """Ancestry population entry."""

    # Dict of form: {<location_id: string>: <percentage: float>}
    populations = mdb.MapField(field=mdb.FloatField(), required=True)


class AncestryResult(mdb.EmbeddedDocument):
    """Set of Ancestry results."""

    # Dict of form: {<sample_id>: <PopulationEntry>}
    samples = mdb.MapField(field=EmDoc(PopulationEntry), required=True)
