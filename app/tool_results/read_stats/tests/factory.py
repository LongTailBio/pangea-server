"""Factory for generating Read Stat result models for testing."""

from random import randint, random

from app.tool_results.read_stats import ReadStatsToolResult


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


def create_read_stats():
    """Create ReadStatsResult with randomized field data."""
    packed_data = create_values()
    return ReadStatsToolResult(**packed_data).save()
