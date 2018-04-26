# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Volcano models for testing."""


from random import random, randint

import factory
from app.display_modules.volcano import VolcanoResult


def make_pval_hist():
    """Return random pval hist."""
    bin_width, nbins = 0.25, 4

    return [{'xval': i * bin_width, 'yval': randint(1, 10)}
            for i in range(nbins)]


def make_scatter_plot():
    """Return random scatter plot."""
    def make_pt():
        """Return a random point."""
        return {
            'xval': randint(-1, 1) * 2 * random(),
            'yval': 2 * random(),
            'zval': random(),
            'name': 'pt_{}'.format(hash(randint(1, 1000))),
        }
    return [make_pt() for _ in range(randint(3, 100))]


def make_tool_category():
    """Return random tool category."""
    return {
        'pval_histogram': make_pval_hist(),
        'scatter_plot': make_scatter_plot(),
    }


def make_tool_doc(categories):
    """Return random tool doc."""
    return {
        'tool_categories': {
            cat_name: {
                cat_val: make_tool_category() for cat_val in cat_vals
            } for cat_name, cat_vals in categories.items()
        }
    }


class VolcanoFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Volcano."""

    class Meta:
        """Factory metadata."""

        model = VolcanoResult

    @factory.lazy_attribute
    def categories(self):  # pylint: disable=no-self-use
        """Generate random categories."""
        return {
            f'cat_name_{i}': [
                f'cat_name_{i}_val_{j}'
                for j in range(randint(3, 6))
            ] for i in range(randint(3, 6))
        }

    @factory.lazy_attribute
    def tools(self):
        """Generate random tool stack."""
        tool_names = ['tool_{}'.format(i) for i in range(randint(3, 6))]
        result = {tool_name: make_tool_doc(self.categories)
                  for tool_name in tool_names}
        return result
