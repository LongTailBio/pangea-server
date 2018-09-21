# pylint: disable=too-few-public-methods disable=no-self-use

"""Factory for generating Kraken result models for testing."""

import random
import factory

from ..models import KrakenResult

DOMAINS = ['archaea', 'bacteria', 'eukarya']
KINGDOMS = ['archaebacteria', 'eubacteria', 'protista', 'fungi',
            'plantae', 'animalia']
PHYLA = ['acanthocephala', 'annelida', 'arthropoda', 'brachiopoda', 'bryozoa',
         'chaetognatha', 'chordata', 'cnidaria', 'ctenophora', 'cycliophora',
         'echinodermata', 'entoprocta', 'gastrotricha', 'gnathostomulida',
         'hemichordata', 'kinorhyncha', 'loricifera', 'micrognathozoa',
         'mollusca', 'nematoda', 'nematomorpha', 'nemertea', 'onychophora',
         'orthonectida', 'phoronida', 'placozoa', 'platyhelminthes',
         'porifera', 'priapulida', 'rhombozoa', 'rotifera', 'sipuncula',
         'tardigrada', 'xenacoelomorpha']


def create_taxa_pair(depth=None):
    """Create taxa name and value for given depth."""
    if depth is None:
        depth = random.randint(1, 5)  # bias distribution towards longer
    entry_name = f'd__{random.choice(DOMAINS)}'
    if depth >= 2:
        entry_name = f'{entry_name}|k__{random.choice(KINGDOMS)}'
    if depth >= 3:
        entry_name = f'{entry_name}|p__{random.choice(PHYLA)}'
    if depth >= 4:  # taxa names do not matter
        entry_name = f'{entry_name}|p__{random.choice(PHYLA)}|s__{random.choice(PHYLA)}'
    value = random.randint(0, 8e07)

    return (entry_name, value)


def create_values(taxa_count=30):
    """Create taxa dictionary."""
    # Make sure we have at least one root element to avoid divide-by-zero
    # https://github.com/bchrobot/metagenscope-server/issues/76
    taxa = dict((create_taxa_pair(depth=1),))
    while len(taxa) < taxa_count - 1:
        taxa.update((create_taxa_pair(),))
    return taxa


def create_result(taxa_count=10, save=True):
    """Create KrakenResult with specified number of taxa."""
    taxa = create_values(taxa_count=taxa_count)
    result = KrakenResult(taxa=taxa)
    if save:
        result.save()
    return result


class KrakenResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = KrakenResult

    @factory.lazy_attribute
    def taxa(self):
        """Return taxa."""
        return create_values()
