# pylint: disable=too-few-public-methods disable=no-self-use

"""Factory for generating HMP tool result models for testing."""

from random import random, randint

import factory

from .. import HmpSitesResult


def create_values():
    """Create plausible data for hmp sites."""
    return {
        'skin': [random() for _ in range(randint(3, 10))],
        'oral': [random() for _ in range(randint(3, 10))],
        'urogenital_tract': [random() for _ in range(randint(3, 10))],
        'airways': [random() for _ in range(randint(3, 10))],
        'gastrointestinal': [random() for _ in range(randint(3, 10))],
    }


class HmpSitesResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = HmpSitesResult

    @factory.lazy_attribute
    def skin(self):
        """Return list of similarities."""
        return [random() for _ in range(randint(3, 10))]

    @factory.lazy_attribute
    def oral(self):
        """Return list of similarities."""
        return [random() for _ in range(randint(3, 10))]

    @factory.lazy_attribute
    def urogenital_tract(self):
        """Return list of similarities."""
        return [random() for _ in range(randint(3, 10))]

    @factory.lazy_attribute
    def airways(self):
        """Return list of similarities."""
        return [random() for _ in range(randint(3, 10))]

    @factory.lazy_attribute
    def gastrointestinal(self):
        """Return list of similarities."""
        return [random() for _ in range(randint(3, 10))]
