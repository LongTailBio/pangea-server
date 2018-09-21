# pylint: disable=too-few-public-methods disable=no-self-use

"""Factory for generating CARD AMR result models for testing."""

from random import randint

import factory

from ..models import CARDAMRToolResult


def simulate_gene():
    """Return one row."""
    gene_name = 'sample_card_amr_gene_{}'.format(randint(1, 100))
    rpk = randint(1, 1000) / 0.66666
    rpkm = randint(1, 1000) / 0.66666
    rpkmg = randint(1, 1000) / 0.66666
    return gene_name, {'rpkm': rpkm, 'rpk': rpk, 'rpkmg': rpkmg}


def create_values():
    """Create CARD AMR values."""
    genes = [simulate_gene() for _ in range(randint(4, 12))]
    out = {gene_name: row_val for gene_name, row_val in genes}
    return out


class CARDAMRToolResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = CARDAMRToolResult

    @factory.lazy_attribute
    def genes(self):
        """Return genes."""
        return create_values()
