"""Factory for generating Humann2 Normalize result models for testing."""

from random import randint

from app.tool_results.humann2_normalize import Humann2NormalizeToolResult


def simulate_gene():
    """Return one row."""
    gene_name = 'sample_humann2_norm_gene_{}'.format(randint(1, 100))
    rpk = randint(1, 1000) / 0.44444
    rpkm = randint(1, 1000) / 0.44444
    rpkmg = randint(1, 1000) / 0.44444
    return gene_name, {'rpkm': rpkm, 'rpk': rpk, 'rpkmg': rpkmg}


def create_values():
    """Create methyl values."""
    genes = [simulate_gene() for _ in range(randint(7, 16))]
    out = {
        'genes': {gene_name: row_val for gene_name, row_val in genes},
    }
    return out


def create_humann2_normalize():
    """Create Huamnn2NormalizeToolResult with randomized field data."""
    packed_data = create_values()
    return Humann2NormalizeToolResult(**packed_data).save()
