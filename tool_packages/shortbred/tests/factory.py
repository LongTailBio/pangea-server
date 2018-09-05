"""Factory for generating Shortbred result models for testing."""

from random import random

from .. import ShortbredResult


def create_values():
    """Create abundance values."""
    abundances = {
        'AAA98484': random() * 5,
        'BAC77251': random() * 5,
        'TEM_137': random() * 50,
        'YP_002317674': random() * 5,
        'YP_310429': random() * 15,
        'soxR_2': random() * 8,
    }
    return {'abundances': abundances}


def create_result(save=True):
    """Create ShortbredResult with randomized field data."""
    packed_data = create_values()
    result = ShortbredResult(**packed_data)
    if save:
        result.save()
    return result
