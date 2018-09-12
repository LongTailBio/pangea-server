"""Taxon Abundance display module."""

import mongoengine as mdb


class TaxonAbundanceNode(mdb.EmbeddedDocument):     # pylint: disable=too-few-public-methods
    """Taxon Abundance node type."""

    id = mdb.StringField(required=True)
    name = mdb.StringField(required=True)
    value = mdb.FloatField(required=True)
    rank = mdb.StringField(required=True)


class TaxonAbundanceEdge(mdb.EmbeddedDocument):     # pylint: disable=too-few-public-methods
    """Taxon Abundance edge type."""

    source = mdb.StringField(required=True)
    target = mdb.StringField(required=True)
    value = mdb.FloatField(required=True)


class TaxonAbundanceFlow(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Taxon Abundance document type."""

    nodes = mdb.ListField(
        mdb.EmbeddedDocumentField(TaxonAbundanceNode),
        required=True
    )
    edges = mdb.EmbeddedDocumentListField(TaxonAbundanceEdge, required=True)

    def clean(self):
        """Ensure that `edges` reference valid nodes."""
        node_ids = {node.id for node in self.nodes}         # pylint: disable=not-an-iterable
        for edge in self.edges:                             # pylint: disable=not-an-iterable
            if edge.source not in node_ids:
                msg = f'Could not find Edge source [{edge.source}] in nodes!'
                raise mdb.ValidationError(msg)
            if edge.target not in node_ids:
                msg = f'Could not find Edge target [{edge.target}] in nodes!'
                raise mdb.ValidationError(msg)


class TaxonAbundanceResult(mdb.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Taxon Abundance document type."""

    by_tool = mdb.MapField(
        field=mdb.EmbeddedDocumentField(TaxonAbundanceFlow),
        required=True
    )
