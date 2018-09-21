# pylint: disable=too-few-public-methods,no-self-use

"""Factory for generating KrakenHLL result models for testing."""

from analysis_packages.base_data.kraken.tests.factory import create_values

import factory

from ..models import KrakenHLLResult


def create_result(taxa_count=10, save=True):
    """Create KrakenHLL Result with specified number of taxa."""
    taxa = create_values(taxa_count=taxa_count)
    result = KrakenHLLResult(taxa=taxa)
    if save:
        result.save()
    return result


class KrakenHLLResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = KrakenHLLResult

    @factory.lazy_attribute
    def taxa(self):
        """Return taxa."""
        return create_values()
