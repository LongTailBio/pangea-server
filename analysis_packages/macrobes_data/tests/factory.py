# pylint: disable=too-few-public-methods,no-self-use

"""Factory for generating Kraken result models for testing."""

from random import randint

import factory

from ..models import MacrobeToolResult


MACROBE_NAMES = ['house cat', 'cow', 'pig', 'chicken']


def simulate_macrobe():
    """Return one row."""
    total_reads = randint(1, 1000)
    rpkm = randint(1, 1000) / 0.33333
    return {'rpkm': rpkm, 'total_reads': total_reads}


def create_values():
    """Create methyl values."""
    macrobe_tbl = {macrobe: simulate_macrobe() for macrobe in MACROBE_NAMES}
    return macrobe_tbl


def create_result(save=True):
    """Create VFDBlToolResult with randomized field data."""
    packed_data = create_values()
    result = MacrobeToolResult(macrobes=packed_data)
    if save:
        result.save()
    return result


class MacrobeToolResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = MacrobeToolResult

    @factory.lazy_attribute
    def macrobes(self):
        """Return macrobes."""
        return create_values()
