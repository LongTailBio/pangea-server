# pylint: disable=too-few-public-methods

"""Factory for generating Beta Diversity models for testing."""

import factory

from tool_packages.beta_diversity.tests.factory import create_values

from app.display_modules.beta_div.models import BetaDiversityResult


class BetaDiversityFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for analysis result's Beta Diversity."""

    class Meta:
        """Factory metadata."""

        model = BetaDiversityResult

    @factory.lazy_attribute
    def data(self):  # pylint:disable=no-self-use
        """Generate a random result."""
        return create_values()
