# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Top Taxa models for testing."""

import factory

from app.display_modules.top_taxa import TopTaxaResult
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.krakenhll.tests.factory import create_krakenhll
from app.tool_results.metaphlan2.tests.factory import create_metaphlan2
from app.tool_results.metaphlan2 import Metaphlan2ResultModule

KRAKENHLL = KrakenHLLResultModule.name()
METAPHLAN = Metaphlan2ResultModule.name()


def create_values():
    """Return values for top taxa sample."""
    return {
        KRAKENHLL: create_krakenhll(),
        METAPHLAN: create_metaphlan2(),
    }


def factory_abundance():
    """Return fake abunds and prevs."""
    return {
        'abundance': {
            'taxa_1': 0.5,
            'taxa_2': 0.2,
            'taxa_3': 0.1,
        },
        'prevalence': {
            'taxa_1': 0.5,
            'taxa_2': 0.8,
            'taxa_3': 0.3,
        }

    }


def factory_tools():
    """Return fake tools."""
    return {
        KRAKENHLL: {
            'all_kingdoms': factory_abundance(),
        },
        METAPHLAN: {
            'all_kingdoms': factory_abundance(),
        },
    }


class TopTaxaFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Sample Similarity."""

    class Meta:
        """Factory metadata."""

        model = TopTaxaResult

    categories = {
        'foo': {
            'foo_1': factory_tools(),
            'foo_2': factory_tools(),
        },
        'bar': {
            'bar_1': factory_tools(),
            'bar_2': factory_tools(),
        },
    }
