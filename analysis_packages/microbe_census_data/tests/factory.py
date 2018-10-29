# pylint: disable=too-few-public-methods,no-self-use

"""Factory for generating Microbe Census result models for testing."""

import random
import factory

from .. import MicrobeCensusResult


def create_values():
    """Create values for Microbe Census result."""
    values = {
        'average_genome_size': random.random() * 10e8,
        'total_bases': random.randint(10e8, 10e10),
        'genome_equivalents': random.random() * 10e2,
    }
    return values


def create_result(save=False):
    """Create MicrobeCensusResult with specified number of taxa."""
    packaged_values = create_values()
    result = MicrobeCensusResult(**packaged_values)
    if save:
        result.save()
    return result


class MicrobeCensusResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = MicrobeCensusResult

    @factory.lazy_attribute
    def average_genome_size(self):
        """Return random ags."""
        return random.random() * 10e8

    @factory.lazy_attribute
    def total_bases(self):
        """Return random total bases."""
        return random.randint(10e8, 10e10)

    @factory.lazy_attribute
    def genome_equivalents(self):
        """Return random number of genome equivalents."""
        return random.random() * 10e2
