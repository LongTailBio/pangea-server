"""Factory for generating Read Stat result models for testing."""

from random import randint, random

import factory

from .. import ReadStatsToolResult


def create_tetramers():
    """Return a dict with plausible values for tetramers."""
    return {'CCCC': randint(100, 1000),
            'TTTT': randint(100, 1000),
            'AAAA': randint(100, 1000),
            'GGGG': randint(100, 1000)}


def create_codons():
    """Return a dict with plausible values for codons.

    Note: this is broken in the CAP, this test reflects the broken state.
    """
    return {'CCC': randint(100, 1000),
            'TTT': randint(100, 1000),
            'AAA': randint(100, 1000),
            'GGG': randint(100, 1000)}


def create_one():
    """Return a dict for one read stats section."""
    return {
        'num_reads': randint(100 * 1000, 1000 * 1000),
        'gc_content': random(),
        'codons': create_codons(),
        'tetramers': create_tetramers(),
    }


def create_values():
    """Create read stat values."""
    return create_one()


def create_result(save=True):
    """Create ReadStatsResult with randomized field data."""
    packed_data = create_values()
    result = ReadStatsToolResult(**packed_data)
    if save:
        result.save()
    return result


class ReadStatsToolResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = ReadStatsToolResult

        @factory.lazy_attribute
        def num_reads(self):
            return randint(100 * 1000, 1000 * 1000)

        @factory.lazy_attribute
        def gc_content(self):
            return random()

        @factory.lazy_attribute
        def codons(self):
            return create_codons()

        @factory.lazy_attribute
        def tetramers(self):
            return create_tetramers()
