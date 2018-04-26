"""Factory for generating artificial Alpha Diversity data."""

from random import random, randint

from app.tool_results.alpha_diversity.models import AlphaDiversityToolResult


def shannon():
    """Return a plausible shannon index."""
    return random() * 4.0 + 1.0


def richness():
    """Return a plausible richness value."""
    return randint(10, 100)


def chao1():
    """Return a plausible chao1 richness value."""
    return richness() + random()


def simpson():
    """Return a plausible gini-simpson index value."""
    return random()


def taxa_level(read_sep=False):
    """Return an object plausible for a taxa level."""
    if read_sep:
        inds = [100 * 1000,
                500 * 1000,
                500 * 1000 + 123456]

        def gen_sep(gen):
            """Generate a value for each index."""
            return {str(ind): gen() for ind in inds}

        return {
            'richness': gen_sep(richness),
            'shannon_index': gen_sep(shannon),
            'gini-simpson': gen_sep(simpson),
            'chao1': gen_sep(chao1),
        }

    return {
        'richness': {'all_reads': richness()},
        'shannon_index': {'all_reads': shannon()},
        'gini-simpson': {'all_reads': simpson()},
    }


def create_values():
    """Return simulated alpha diversity data."""
    return {
        'metaphlan2': {
            'species': taxa_level(),
            'genus': taxa_level(),
        }, 'kraken': {
            'species': taxa_level(read_sep=True),
            'genus': taxa_level(read_sep=True),
        }
    }


def create_alpha_diversity():
    """Return an alpha diversity result with simulated data."""
    packed_data = create_values()
    return AlphaDiversityToolResult(**packed_data)
