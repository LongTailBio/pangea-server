"""Factory for generating Microbe Census result models for testing."""

import random

from app.tool_results.microbe_census import MicrobeCensusResult


def create_microbe_census():
    """Create MicrobeCensusResult with specified number of taxa."""
    return MicrobeCensusResult(average_genome_size=random.random() * 10e8,
                               total_bases=random.randint(10e8, 10e10),
                               genome_equivalents=random.random() * 10e2).save()
