# pylint: disable=too-few-public-methods,no-self-use

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


class AncestryToolResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = AncestryToolResult

    @factory.lazy_attribute
    def populations(self):
        """Return populations."""
        return create_values()
