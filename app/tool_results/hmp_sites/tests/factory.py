"""Factory for generating HMP tool result models for testing."""

from random import random, randint

from app.tool_results.hmp_sites import HmpSitesResult


def create_values():
    """Create plausible data for hmp sites."""
    return {
        'skin': [random() for _ in range(randint(3, 10))],
        'oral': [random() for _ in range(randint(3, 10))],
        'urogenital_tract': [random() for _ in range(randint(3, 10))],
        'airways': [random() for _ in range(randint(3, 10))],
        'gastrointestinal': [random() for _ in range(randint(3, 10))],
    }


def create_hmp_sites():
    """Create HmpSitesResult with randomized fields."""
    packed_data = create_values()
    return HmpSitesResult(**packed_data).save()
