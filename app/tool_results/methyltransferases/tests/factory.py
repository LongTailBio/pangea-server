"""Factory for generating Kraken result models for testing."""

from random import randint

from app.tool_results.methyltransferases import MethylToolResult


def simulate_gene():
    """Return one row."""
    gene_name = 'sample_gene_{}'.format(randint(1, 100))
    rpk = randint(1, 100) / 0.33333
    rpkm = randint(1, 100) / 0.33333
    rpkmg = randint(1, 100) / 0.33333
    return gene_name, {'rpk': rpk, 'rpkm': rpkm, 'rpkmg': rpkmg}


def create_values():
    """Create methyl values."""
    genes = [simulate_gene() for _ in range(randint(3, 10))]
    result = {
        'genes': {gene_name: row for gene_name, row in genes}

    }
    return result


def create_methyls():
    """Create MethylToolResult with randomized field data."""
    packed_data = create_values()
    return MethylToolResult(**packed_data).save()
