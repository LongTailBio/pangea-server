# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Average Genome Size models for testing."""

import factory

from analysis_packages.base.models import DistributionResult

from ..models import AGSResult


class DistributionFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Sample Similarity's tool."""

    class Meta:
        """Factory metadata."""

        model = DistributionResult

    min_val = 0
    q1_val = 1
    mean_val = 2
    q3_val = 3
    max_val = 4


class AGSFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Sample Similarity."""

    class Meta:
        """Factory metadata."""

        model = AGSResult

    @factory.lazy_attribute
    def categories(self):  # pylint: disable=no-self-use
        """Generate random categories."""
        category_name = factory.Faker('word').generate({})
        return {category_name: factory.Faker('words', nb=4).generate({})}

    @factory.lazy_attribute
    def distributions(self):
        """Generate distributions for categories."""
        result = {}
        for category_name, category_values in self.categories.items():
            result[category_name] = {}
            for category_value in category_values:
                result[category_name][category_value] = DistributionFactory()
        return result
