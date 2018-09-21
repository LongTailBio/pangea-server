# pylint: disable=too-few-public-methods,no-self-use

"""Factory for generating Kraken result models for testing."""

from random import randint, random

from .. import Humann2Result


def random_pathway():
    """Return a plausible pair of values for a sample pathway."""
    return {
        'abundance': 100 * random(),
        'coverage': random(),
    }


def create_values():
    """Create a plausible humann2 values object."""
    result = {'sample_pathway_{}': random_pathway()
              for i in range(randint(3, 100))}
    return result


def create_result(save=True):
    """Create Humann2Result with randomized field data."""
    packed_data = create_values()
    result = Humann2Result(pathways=packed_data)
    if save:
        result.save()
    return result


class Humann2ResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = Humann2Result

    @factory.lazy_attribute
    def pathways(self):
        """Return pathways."""
        return create_values()
