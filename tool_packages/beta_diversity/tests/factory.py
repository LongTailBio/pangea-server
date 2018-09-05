"""Factory for generating artificial beta diversity results."""

from random import randint, random

from ..models import BetaDiversityToolResult


def generate_sample_names():
    """Return a list of sample names."""
    num_samples = randint(3, 6)
    return ['test_sample_{}'.format(i) for i in range(num_samples)]


def jsd():
    """Return a plausible value for jensen shannon distance."""
    return random()


def rhop():
    """Return a plausible value for rho proportionality."""
    if random() < 0.5:
        return -1 * random()
    return random()


def one_matrix(snames, gen, reflexive=0):
    """Create a distance matrix with the given generator."""
    distm = {}
    for name1 in snames:
        distm[name1] = {}
        for name2 in snames:
            if name1 == name2:
                distm[name1][name2] = reflexive
            else:
                try:
                    distm[name1][name2] = distm[name2][name1]
                except KeyError:
                    distm[name1][name2] = gen()
    return distm


def taxa_level(snames):
    """Return plausible values for one taxa level."""
    return {
        'jensen_shannon_distance': {
            'metaphlan2': one_matrix(snames, jsd),
            'kraken': one_matrix(snames, jsd),
        },
        'rho_proportionality': {
            'metaphlan2': one_matrix(snames, rhop, reflexive=1),
            'kraken': one_matrix(snames, rhop, reflexive=1),
        },
    }


def create_values():
    """Return simulated beta diversity data."""
    sample_names = generate_sample_names()
    return {
        'species': taxa_level(sample_names),
        'genus': taxa_level(sample_names),
    }


def create_result(save=True):
    """Return a beta diversity result with simulated data."""
    ranks = create_values()
    result = BetaDiversityToolResult(data=ranks)
    if save:
        result.save()
    return result
