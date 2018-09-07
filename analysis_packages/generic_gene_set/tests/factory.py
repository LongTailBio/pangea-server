# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

from random import randint

import factory


def randvalue():
    """Create random value."""
    return float(randint(0, 70) / 10)


def create_one_sample():
    """Return an example sample for VFDBResult."""
    return {
        'rpkm': {'sample_gene_1': randvalue(), 'sample_gene_2': randvalue()},
        'rpkmg': {'sample_gene_1': randvalue(), 'sample_gene_2': randvalue()},
    }


class GeneSetFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Microbe Directory."""

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample_{i}'] = create_one_sample()
        return samples
