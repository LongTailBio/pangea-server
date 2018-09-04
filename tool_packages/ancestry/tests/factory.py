"""Factory for generating Ancestry result models for testing."""

from random import random

from .. import AncestryToolResult
from ..constants import KNOWN_LOCATIONS


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


def create_result():
    """Create AncestryToolResult with randomized field data."""
    packed_data = {'populations': create_values()}
    return AncestryToolResult(**packed_data).save()
