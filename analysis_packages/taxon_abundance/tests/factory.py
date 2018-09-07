"""Factory for generating Taxon Abundance models for testing."""

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


def create_taxon_abundance():
    """Ensure Taxon Abundance model is created correctly."""
    taxon_abundance = TaxonAbundanceResult(**{
        'by_tool': {
            'kraken': flow_model(),
            'metaphlan2': flow_model()
        }
    })