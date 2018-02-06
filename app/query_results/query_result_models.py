"""Query Result model definitions."""

import datetime

from mongoengine import ValidationError

from app.extensions import mongoDB


QUERY_RESULT_STATUS = (('E', 'ERROR'),
                       ('P', 'PENDING'),
                       ('W', 'WORKING'),
                       ('S', 'SUCCESS'))


# pylint: disable=too-few-public-methods
class QueryResultWrapper(mongoDB.EmbeddedDocument):
    """Base mongo result class."""

    status = mongoDB.StringField(required=True,
                                 max_length=1,
                                 choices=QUERY_RESULT_STATUS,
                                 default='P')

    meta = {'allow_inheritance': True}


class ToolDocument(mongoDB.EmbeddedDocument):
    """Tool document type."""

    x_label = mongoDB.StringField(required=True)
    y_label = mongoDB.StringField(required=True)


class SampleSimilarityResult(mongoDB.EmbeddedDocument):
    """Sample Similarity document type."""

    categories = mongoDB.MapField(field=mongoDB.ListField(mongoDB.StringField()), required=True)
    tools = mongoDB.MapField(field=mongoDB.EmbeddedDocumentField(ToolDocument), required=True)
    data_records = mongoDB.ListField(mongoDB.DictField(), required=True)

    def clean(self):
        """Ensure that `data_records` contain valid records."""
        category_names = self.categories.keys()
        tool_names = self.tools.keys()

        for record in self.data_records:
            for category_name in category_names:
                if category_name not in record:
                    msg = 'Record must have all categories.'
                    raise ValidationError(msg)
            for tool_name in tool_names:
                if '%s_x' % tool_name not in record or '%s_y' % tool_name not in record:
                    msg = 'Record must x and y for all tools.'
                    raise ValidationError(msg)


class SampleSimilarityResultWrapper(QueryResultWrapper):
    """Status wrapper for Sample Similarity document type."""

    data = mongoDB.EmbeddedDocumentField(SampleSimilarityResult)


class TaxonAbundanceNode(mongoDB.EmbeddedDocument):
    """Taxon Abundance node type."""

    id = mongoDB.StringField(required=True)
    name = mongoDB.StringField(required=True)
    value = mongoDB.FloatField(required=True)


class TaxonAbundanceEdge(mongoDB.EmbeddedDocument):
    """Taxon Abundance edge type."""

    source = mongoDB.StringField(required=True)
    target = mongoDB.StringField(required=True)
    value = mongoDB.FloatField(required=True)


class TaxonAbundanceResult(mongoDB.EmbeddedDocument):
    """Taxon Abundance document type."""

    # Do not store depth of node because this can be derived from the edges
    nodes = mongoDB.EmbeddedDocumentListField(TaxonAbundanceNode, required=True)
    edges = mongoDB.EmbeddedDocumentListField(TaxonAbundanceEdge, required=True)

    def clean(self):
        """Ensure that `edges` reference valid nodes."""
        node_ids = set([node.id for node in self.nodes])
        for edge in self.edges:
            if edge.source not in node_ids:
                msg = f'Could not find Edge\'s source [{edge.source}] in nodes!'
                raise ValidationError(msg)
            if edge.target not in node_ids:
                msg = f'Could not find Edge\'s target [{edge.target}] in nodes!'
                raise ValidationError(msg)


class TaxonAbundanceResultWrapper(QueryResultWrapper):
    """Status wrapper for Taxon Abundance document type."""

    data = mongoDB.EmbeddedDocumentField(TaxonAbundanceResult)


class ReadsClassifiedDatum(mongoDB.EmbeddedDocument):
    """Taxon Abundance datum type."""

    category = mongoDB.StringField(required=True)
    values = mongoDB.ListField(mongoDB.FloatField(), required=True)


class ReadsClassifiedResult(mongoDB.EmbeddedDocument):
    """Reads Classified document type."""

    categories = mongoDB.ListField(mongoDB.StringField(), required=True)
    sample_names = mongoDB.ListField(mongoDB.StringField(), required=True)
    data = mongoDB.EmbeddedDocumentListField(ReadsClassifiedDatum, required=True)

    def clean(self):
        """Ensure integrity of result content."""
        for datum in self.data:
            if datum.category not in self.categories:
                msg = f'Datum category \'{datum.category}\' does no exist in categories!'
                raise ValidationError(msg)
            if len(datum.values) != len(self.sample_names):
                msg = (f'Number of datum values for \'{datum.category}\''
                       'does not match sample_names length!')
                raise ValidationError(msg)


class ReadsClassifiedResultWrapper(QueryResultWrapper):
    """Status wrapper for Reads Classified document type."""

    data = mongoDB.EmbeddedDocumentField(ReadsClassifiedResult)


class HMPDatum(mongoDB.EmbeddedDocument):
    """HMP datum type."""

    name = mongoDB.StringField(required=True)
    data = mongoDB.ListField(mongoDB.ListField(mongoDB.FloatField()), required=True)


class HMPResult(mongoDB.EmbeddedDocument):
    """HMP document type."""

    categories = mongoDB.MapField(field=mongoDB.ListField(mongoDB.StringField()), required=True)
    sites = mongoDB.ListField(mongoDB.StringField(), required=True)
    data = mongoDB.MapField(field=mongoDB.EmbeddedDocumentListField(HMPDatum), required=True)

    def clean(self):
        """Ensure integrity of result content."""
        for category, values in self.categories.items():
            if category not in self.data:
                msg = f'Value \'{category}\' is not present in \'data\'!'
                raise ValidationError(msg)
            values_present = [datum.name for datum in self.data[category]]
            for value in values:
                if value not in values_present:
                    msg = f'Value \'{category}\' is not present in \'data\'!'
                    raise ValidationError(msg)

        for category_name, category_data in self.data.items():
            if len(category_data) != len(self.categories[category_name]):
                msg = (f'Category data for {category_name} does not match size of '
                       f'category values ({len(self.categories[category_name])})!')
                raise ValidationError(msg)
            for datum in category_data:
                if len(datum.data) != len(self.sites):
                    msg = (f'Datum <{datum.name}> of size {len(datum.data)} '
                           f'does not match size of sites ({len(self.sites)})!')
                    raise ValidationError(msg)


class HMPResultWrapper(QueryResultWrapper):
    """Status wrapper for HMP document type."""

    data = mongoDB.EmbeddedDocumentField(HMPResult)


class QueryResultMeta(mongoDB.Document):
    """Base mongo result class."""

    sample_group_id = mongoDB.UUIDField(binary=False)
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    sample_similarity = mongoDB.EmbeddedDocumentField(SampleSimilarityResultWrapper)
    taxon_abundance = mongoDB.EmbeddedDocumentField(TaxonAbundanceResultWrapper)
    reads_classified = mongoDB.EmbeddedDocumentField(ReadsClassifiedResultWrapper)
    hmp = mongoDB.EmbeddedDocumentField(HMPResultWrapper)

    meta = {
        'indexes': ['sample_group_id']
    }

    @property
    def result_types(self):
        """Return a list of all query result types available for this record."""
        blacklist = ['id', 'sample_group_id', 'created_at']
        all_fields = [k for k, v in self.__class__._fields.items() if k not in blacklist]
        return [field for field in all_fields if hasattr(self, field)]
