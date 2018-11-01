"""Factory for generating Reads CLassified result models for testing."""

from random import random

from .. import ReadsClassifiedToolResult


def create_values():
    """Create reads classified values."""
    return {
        'viral': random(),
        'archaeal': random(),
        'bacterial': random(),
        'host': random(),
        'nonhost_macrobial': random(),
        'fungal': random(),
        'nonfungal_eukaryotic': random(),
        'unknown': random(),
        'total': random(),
    }


def create_result(save=True):
    """Create ReadStatsResult with randomized field data."""
    packed_data = create_values()
    result = ReadsClassifiedToolResult(**packed_data)
    if save:
        result.save()
    return result
