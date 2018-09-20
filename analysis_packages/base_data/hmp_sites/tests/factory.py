"""Factory for generating HMP tool result models for testing."""

from random import random, randint

from .. import HmpSitesResult


def create_values():
    """Create plausible data for hmp sites."""
    return {
        'skin': [random() for _ in range(randint(3, 10))],
        'oral': [random() for _ in range(randint(3, 10))],
        'urogenital_tract': [random() for _ in range(randint(3, 10))],
        'airways': [random() for _ in range(randint(3, 10))],
        'gastrointestinal': [random() for _ in range(randint(3, 10))],
    }


def create_result(save=True):
    """Create HmpSitesResult with randomized fields."""
    packed_data = create_values()
    result = HmpSitesResult(**packed_data)
    if save:
        result.save()
    return result
