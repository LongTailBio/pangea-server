# pylint: disable=too-few-public-methods disable=no-self-use

"""Factory for generating Kraken result models for testing."""

from random import randint

import factory

from ..models import MethylToolResult


def simulate_gene():
    """Return one row."""
    gene_name = 'sample_gene_{}'.format(randint(1, 100))
    rpk = randint(1, 100) / 0.33333
    rpkm = randint(1, 100) / 0.33333
    rpkmg = randint(1, 100) / 0.33333
    return gene_name, {'rpk': rpk, 'rpkm': rpkm, 'rpkmg': rpkmg}


def create_values():
    """Create methyl values."""
    genes = [simulate_gene() for _ in range(randint(3, 10))]
    result = {gene_name: row for gene_name, row in genes}
    return result


def create_result(save=True):
    """Create MethylToolResult with randomized field data."""
    packed_data = create_values()
    result = MethylToolResult(genes=packed_data)
    if save:
        result.save()
    return result


class MethylToolResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = MethylToolResult

    @factory.lazy_attribute
    def genes(self):
        """Return random genes."""
        return create_values()
