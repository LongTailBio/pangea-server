"""Volcano display models."""

from app.extensions import mongoDB as mdb


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name


class XYZPoint(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Represent a 3d point."""

    xval = mdb.FloatField(required=True)
    yval = mdb.FloatField(required=True)
    zval = mdb.FloatField(default=1)
    name = mdb.StringField()


class ToolCategoryDocument(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """The base data type that generates a particular plot."""

    pval_histogram = mdb.ListField(EmbeddedDoc(XYZPoint))
    scatter_plot = mdb.ListField(EmbeddedDoc(XYZPoint), required=True)


class ToolDocument(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Organize all 'plots' from a particular tool."""

    tool_categories = mdb.MapField(
        field=mdb.MapField(field=EmbeddedDoc(ToolCategoryDocument)),
        required=True
    )


class VolcanoResult(mdb.EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Volcano document type."""

    # Categories dict is of the form: {<category_name>: [<category_value>, ...]}
    categories = mdb.MapField(field=StringList)
    # Tools dict is of the form: {<tool_name>: <ToolDocument>}
    tools = mdb.MapField(field=EmbeddedDoc(ToolDocument))
