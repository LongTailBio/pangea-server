# pylint: disable=missing-docstring,too-few-public-methods,no-self-use

"""Factory for generating HMP models for testing."""

from random import random, randint

import factory

from ..models import HMPResult


def fake_distribution():
    """Return a random 'distribution'."""
    distribution = [random() for _ in range(5)]
    return sorted(distribution)


def fake_categories():
    """Return fake categories."""
    out = {}
    for category_name in ['cat_1', 'cat_2']:
        out[category_name] = []
        for i in range(randint(2, 4)):
            out[category_name].append(category_name + str(i))
    return out


def fake_sites():
    """Return fake sites."""
    return ['skin', 'oral', 'urogenital', 'airways']


class HMPFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's HMP."""

    class Meta:
        """Factory metadata."""

        model = HMPResult

    @factory.lazy_attribute
    def categories(self):
        """Return categories."""
        return fake_categories()

    @factory.lazy_attribute
    def sites(self):
        """Return body sites."""
        return fake_sites()

    @factory.lazy_attribute
    def data(self):
        """Return plausible data."""
        out = {}
        for category_name, category_values in self.categories.items():
            out[category_name] = []
            for category_value in category_values:
                datum = {
                    'name': category_value,
                    'data': [fake_distribution() for _ in self.sites],
                }
                out[category_name].append(datum)
        return out
