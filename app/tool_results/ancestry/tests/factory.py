"""Factory for generating Ancestry result models for testing."""

from random import random

from app.tool_results.ancestry import AncestryToolResult
from app.tool_results.ancestry.constants import KNOWN_LOCATIONS


def create_values(dropout=0.25):
    """Create ancestry values."""
    result = {}
    tot = 0
    for loc in KNOWN_LOCATIONS:
        if random() < dropout:
            val = random()
            result[loc] = val
            tot += val
    return {loc: val / tot for loc, val in result.items()}


def create_ancestry():
    """Create AncestryToolResult with randomized field data."""
    packed_data = {'populations': create_values()}
    return AncestryToolResult(**packed_data).save()
