# pylint: disable=too-few-public-methods

"""Factory for generating Alpha Diversity models for testing."""

from random import randint

import factory

from ..models import AlphaDiversityResult


def get_from_dict_or_obj(obj, key):
    """Get a key from a dict or a mongoengine object."""
    try:
        return obj[key]
    except TypeError:
        return getattr(obj, key)


def create_categories():
    """Generate a random result for categories."""
    result = {
        'category00': ['value00', 'value01', 'value02']
    }
    return result


def create_tools():
    """Generate random result for tools."""
    return ['tool00', 'tool01']


def create_by_tool(factory_self):
    """Generate random result for by_tools."""
    result = {}

    def create_by_metric(metrics):
        """Generate by_metric."""
        by_metric_result = {}
        for metric in metrics:
            distribution = [randint(0, 15) for i in range(5)]
            distribution.sort()
            by_metric_result[metric] = distribution
        return by_metric_result

    def create_by_categories(categories):
        """Generate by_category_name."""
        by_category_result = {}
        for index, category in enumerate(categories):
            metrics = ['metric00', 'metric01']
            by_category_result[category] = [{
                'metrics': metrics,
                'category_value': f'value0{index}',
                'by_metric': create_by_metric(metrics),
            } for _ in range(3)]
        return by_category_result

    def create_by_taxa_rank(taxa_ranks):
        """Generate taxa_by_rank."""
        by_rank_result = {}
        for taxa_rank in taxa_ranks:
            cats = get_from_dict_or_obj(factory_self, 'categories')
            by_rank_result[taxa_rank] = {
                'by_category_name': create_by_categories(cats)
            }
        return by_rank_result

    for tool in get_from_dict_or_obj(factory_self, 'tool_names'):
        taxa_ranks = ['taxa00']
        result[tool] = {
            'taxa_ranks': taxa_ranks,
            'by_taxa_rank': create_by_taxa_rank(taxa_ranks),
        }

    return result


class AlphaDivFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for analysis result's Alpha diversity."""

    class Meta:
        """Factory metadata."""

        model = AlphaDiversityResult

    @factory.lazy_attribute
    def categories(self):  # pylint: disable=no-self-use
        """Generate a random result for categories."""
        return create_categories()

    @factory.lazy_attribute
    def tool_names(self):  # pylint: disable=no-self-use
        """Generate random result for tools."""
        return create_tools()

    @factory.lazy_attribute
    def by_tool(self):
        """Generate random result for by_tools."""
        return create_by_tool(self)
