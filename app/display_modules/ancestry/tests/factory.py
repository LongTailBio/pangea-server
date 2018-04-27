# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

from pandas import DataFrame

import factory

from app.display_modules.ancestry import AncestryResult
from app.tool_results.ancestry.tests.factory import create_values


class AncestryFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Microbe Directory."""

    class Meta:
        """Factory metadata."""

        model = AncestryResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_values()

        samples = DataFrame(samples).fillna(0).to_dict()
        return samples
