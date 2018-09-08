"""Factory for generating Taxon Abundance models for testing."""

import factory

from ..models import TaxonAbundanceResult


def flow_model():
    """Return an example flow model."""
    return {
        'nodes': [
            {
                'id': 'left_root',
                'name': 'left_root',
                'value': 3.5,
                'rank': 'l',
            },
            {
                'id': 'right_root',
                'name': 'right_root',
                'value': 3.5,
                'rank': 'r',
            },
        ], 'edges': [
            {
                'source': 'left_root',
                'target': 'right_root',
                'value': 1.0,
            },
        ]
    }


class TaxonAbundanceFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Taxon Abundance."""

    class Meta:
        """Factory metadata."""

        model = TaxonAbundanceResult

    @factory.lazy_attribute
    def by_tool(self):  # pylint: disable=no-self-use
        """Generate flow modles by tool."""
        return {
            'kraken': flow_model(),
            'metaphlan2': flow_model()
        }
