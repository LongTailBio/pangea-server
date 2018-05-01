"""Factory for generating Kraken result models for testing."""

from random import randint, random

from app.tool_results.humann2 import Humann2Result


def random_pathway():
    """Return a plausible pair of values for a sample pathway."""
    return {
        'abundance': 100 * random(),
        'coverage': random()
    }


def create_values():
    """Create a plausible humann2 values object."""
    result = {
        'pathways': {'sample_pathway_{}': random_pathway()
                     for i in range(randint(3, 100))},
    }
    return result


def create_humann2():
    """Create Humann2Result with randomized field data."""
    packed_data = create_values()
    return Humann2Result(**packed_data).save()
