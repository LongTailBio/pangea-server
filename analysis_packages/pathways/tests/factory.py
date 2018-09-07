# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Pathway models for testing."""

from random import random, randint

import factory

from ..models import PathwayResult


def create_one_sample():
    """Create one random, plausible sample."""
    paths = ['sample_path_{}'.format(i) for i in range(randint(3, 10))]
    sample = {'pathway_abundances': {}, 'pathway_coverages': {}}
    for path in paths:
        sample['pathway_abundances'][path] = 100 * random()
        sample['pathway_coverages'][path] = random()
    return sample


class PathwayFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Pathway."""

    class Meta:
        """Factory metadata."""

        model = PathwayResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_one_sample()
        return samples
