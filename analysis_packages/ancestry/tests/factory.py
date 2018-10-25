# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Ancestry models for testing."""

from pandas import DataFrame

import factory

from analysis_packages.base_data.ancestry.tests.factory import create_values

from ..models import AncestryResult


def create_result():
    """Spoof ancestry result."""
    samples = {}
    for i in range(10):
        samples[f'Sample{i}'] = {'populations': create_values()}

    samples = DataFrame(samples).fillna(0).to_dict()
    return samples

class AncestryFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for generating Ancestry models for testing."""

    class Meta:
        """Factory metadata."""

        model = AncestryResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random Samples."""
        return create_result()
