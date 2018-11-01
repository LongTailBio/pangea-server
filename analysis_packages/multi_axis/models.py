"""Multi Axis display models."""

import mongoengine as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name


class AxisDocument(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Tool document type."""

    vals = mdb.MapField(field=mdb.FloatField(), required=True)


class MultiAxisResult(mdb.EmbeddedDocument):     # pylint: disable=too-few-public-methods
    """Multi Axis document type."""

    # Categories dict is of the form: {<category_name>: [<category_value>, ...]}
    categories = mdb.MapField(field=StringList, required=True)
    axes = mdb.MapField(field=EmbeddedDoc(AxisDocument), required=True)
    metadata = mdb.MapField(
        field=mdb.MapField(field=mdb.StringField(), required=True),
        required=True
    )
