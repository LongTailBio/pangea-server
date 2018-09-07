# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating ReadStats models for testing."""

import factory

from tool_packages.read_stats.tests.factory import create_values

from app.display_modules.read_stats import ReadStatsResult


class ReadStatsFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Read Stats."""

    class Meta:
        """Factory metadata."""

        model = ReadStatsResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_values()
        return samples
