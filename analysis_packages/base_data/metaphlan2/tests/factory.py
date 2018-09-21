# pylint: disable=too-few-public-methods,no-self-use

"""Factory for generating Metaphlan2 result models for testing."""

from tool_packages.kraken.tests.factory import create_values

import factory

from ..models import Metaphlan2Result


def create_result(taxa_count=10, save=True):
    """Create Metaphlan2Result with specified number of taxa."""
    taxa = create_values(taxa_count=taxa_count)
    result = Metaphlan2Result(taxa=taxa)
    if save:
        result.save()
    return result


class Metaphlan2ResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = Metaphlan2Result

    @factory.lazy_attribute
    def taxa(self):
        """Return taxa."""
        return create_values()
