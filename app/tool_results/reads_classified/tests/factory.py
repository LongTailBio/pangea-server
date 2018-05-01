"""Factory for generating Reads CLassified result models for testing."""

from random import randint

from app.tool_results.reads_classified import ReadsClassifiedToolResult


def create_values():
    """Create reads classified values."""
    return {
        'viral': randint(1000, 1000 * 1000),
        'archaeal': randint(1000, 1000 * 1000),
        'bacterial': randint(1000, 1000 * 1000),
        'host': randint(1000, 1000 * 1000),
        'nonhost_macrobial': randint(1000, 1000 * 1000),
        'fungal': randint(1000, 1000 * 1000),
        'nonfungal_eukaryotic': randint(1000, 1000 * 1000),
        'unknown': randint(1000, 1000 * 1000),
        'total': randint(1000, 1000 * 1000),
    }


def create_read_stats():
    """Create ReadStatsResult with randomized field data."""
    packed_data = create_values()
    return ReadsClassifiedToolResult(**packed_data).save()
