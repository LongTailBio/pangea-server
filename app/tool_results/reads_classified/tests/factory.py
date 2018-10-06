"""Factory for generating Reads CLassified result models for testing."""

from random import random

from app.tool_results.reads_classified import ReadsClassifiedToolResult


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


def create_read_stats():
    """Create ReadStatsResult with randomized field data."""
    packed_data = create_values()
    return ReadsClassifiedToolResult(**packed_data).save()
