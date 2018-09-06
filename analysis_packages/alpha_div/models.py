# pylint: disable=too-few-public-methods

"""Models for AlphaDiversity AnalysisModule."""

import mongoengine as mdb

# Define aliases
EmDoc = mdb.EmbeddedDocumentField               # pylint: disable=invalid-name
EmDocList = mdb.EmbeddedDocumentListField       # pylint: disable=invalid-name


class AlphaDiversityDatum(mdb.EmbeddedDocument):
    """AlphaDiv datum type."""

    metrics = mdb.ListField(mdb.StringField())
    category_value = mdb.StringField(required=True)
    # metric -> distribution
    by_metric = mdb.MapField(field=mdb.ListField(mdb.FloatField()))


class AlphaDiversityRank(mdb.EmbeddedDocument):
    """Store a map of cat_name -> [(cat_value, metric -> distribution)]."""

    by_category_name = mdb.MapField(field=EmDocList(AlphaDiversityDatum),
                                    required=True)


class AlphaDiversityTool(mdb.EmbeddedDocument):
    """Store a map of rank -> AlphaDiversityRank."""

    taxa_ranks = mdb.ListField(mdb.StringField())
    by_taxa_rank = mdb.MapField(field=EmDoc(AlphaDiversityRank))


class AlphaDiversityResult(mdb.EmbeddedDocument):
    """Embedded results for alpha diversity."""

    # Categories dict has form: {<category_name>: [<category_value>, ...]}
    categories = mdb.MapField(field=mdb.ListField(mdb.StringField()), required=True)
    tool_names = mdb.ListField(mdb.StringField())
    by_tool = mdb.MapField(field=EmDoc(AlphaDiversityTool), required=True)
