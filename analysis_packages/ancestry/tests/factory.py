# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Ancestry models for testing."""

from pandas import DataFrame

import factory

from tool_packages.ancestry.tests.factory import create_values

from ..models import AncestryResult


class AncestryFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for generating Ancestry models for testing."""

    class Meta:
        """Factory metadata."""

        model = AncestryResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = {'populations': create_values()}

        samples = DataFrame(samples).fillna(0).to_dict()
        return samples
