# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Read Classified models for testing."""

import factory

from tool_packages.reads_classified.tests.factory import create_values

from ..models import ReadsClassifiedResult


def create_vals_no_total():
    """Create a reads classified proportion without total."""
    return {key: val
            for key, val in create_values().items()
            if key != 'total'}


class ReadsClassifiedFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Read Stats."""

    class Meta:
        """Factory metadata."""

        model = ReadsClassifiedResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_vals_no_total()
        return samples
