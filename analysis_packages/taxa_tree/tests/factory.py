# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Taxa Tree models for testing."""

from random import random, randint

import factory

from ..models import TaxaTreeResult


def generate_random_tree(parent=None, level=0, parent_size=100, ind=0):
    """Return a random, plausible, taxa tree."""
    if parent is None:
        parent_name = None
        name = 'root'
        parent_size = 100
        parent_list = name
        size = 100
    else:
        name = 'level_{}_{}'.format(level, ind)
        size = random() * parent_size
        parent_name = parent.split('|')[-1]
        parent_list = parent + '|' + name
    children = []
    if random() < (1 / (level + 1)):
        children = [
            generate_random_tree(
                parent=parent_list,
                level=level + 1,
                parent_size=size,
                ind=i,
            )
            for i in range(randint(3, 6))
        ]

    return {
        'name': name,
        'size': size,
        'parent': parent_name,
        'children': children
    }


class TaxaTreeFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for TaxaTree's Read Stats."""

    class Meta:
        """Factory metadata."""

        model = TaxaTreeResult

    @factory.lazy_attribute
    def metaphlan2(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        return generate_random_tree()

    @factory.lazy_attribute
    def kraken(self):  # pylint: disable=no-self-use
        """Generate random kraken."""
        return generate_random_tree()

    @factory.lazy_attribute
    def krakenhll(self):  # pylint: disable=no-self-use
        """Generate random krakenhll."""
        return generate_random_tree()
