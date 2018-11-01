"""Models for pathways."""

import mongoengine as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name


class PathwaySampleDocument(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Pathway for a single sample."""

    pathway_abundances = mdb.MapField(mdb.FloatField(), required=True)
    pathway_coverages = mdb.MapField(mdb.FloatField(), required=True)


class PathwayResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Set of pathway results."""

    samples = mdb.MapField(field=EmbeddedDoc(PathwaySampleDocument), required=True)
