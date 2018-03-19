# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

import factory

from app.display_modules.microbe_directory import MicrobeDirectoryResult
from app.tool_results.microbe_directory.tests.factory import create_values


class MicrobeDirectoryFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Microbe Directory."""

    class Meta:
        """Factory metadata."""

        model = MicrobeDirectoryResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_values()
        return samples
