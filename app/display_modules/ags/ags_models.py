# pylint: disable=too-few-public-methods

"""Average Genome Size display models."""

from app.extensions import mongoDB as mdb
from app.display_modules.shared_models import DistributionResult


# Define aliases
EmbeddedDoc = mdb.EmbeddedDocumentField         # pylint: disable=invalid-name
StringList = mdb.ListField(mdb.StringField())   # pylint: disable=invalid-name


class AGSResult(mdb.EmbeddedDocument):
    """AGS document type."""

    # Categories dict has form: {<category_name>: [<category_value>, ...]}
    categories = mdb.MapField(field=StringList, required=True)
    # Distribution dict has form: {<category_name>: {<category_value>: <dist>}}
    distributions = mdb.MapField(field=mdb.MapField(field=EmbeddedDoc(DistributionResult)),
                                 required=True)
