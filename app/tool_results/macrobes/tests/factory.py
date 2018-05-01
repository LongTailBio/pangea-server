"""Factory for generating Kraken result models for testing."""

from random import randint

from app.tool_results.macrobes import MacrobeToolResult


MACROBE_NAMES = ['house cat', 'cow', 'pig', 'chicken']


def simulate_macrobe():
    """Return one row."""
    total_reads = randint(1, 1000)
    rpkm = randint(1, 1000) / 0.33333
    return {'rpkm': rpkm, 'total_reads': total_reads}


def create_values():
    """Create methyl values."""
    macrobe_tbl = {macrobe: simulate_macrobe() for macrobe in MACROBE_NAMES}
    out = {
        'macrobes': macrobe_tbl,
    }
    return out


def create_macrobe():
    """Create VFDBlToolResult with randomized field data."""
    packed_data = create_values()
    return MacrobeToolResult(**packed_data).save()
