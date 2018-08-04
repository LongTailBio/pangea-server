"""Multi Axis display models."""

from app.extensions import mongoDB as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name


class AxisDocument(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Tool document type."""

    axis_label = mdb.StringField(required=True)
    mdb.MapField(field=mdb.FloatField, required=True)


class SampleSimilarityResult(mdb.EmbeddedDocument):     # pylint: disable=too-few-public-methods
    """Sample Similarity document type."""

    # Categories dict is of the form: {<category_name>: [<category_value>, ...]}
    categories = mdb.MapField(field=StringList, required=True)
    axes = mdb.MapField(field=EmbeddedDoc(AxisDocument), required=True)
