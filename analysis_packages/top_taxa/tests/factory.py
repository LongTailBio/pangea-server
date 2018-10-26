# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Top Taxa models for testing."""

from random import random

import factory

from analysis_packages.krakenhll_data import KrakenHLLResultModule
from analysis_packages.krakenhll_data.tests.factory import create_result as create_krakenhll
from analysis_packages.metaphlan2_data.tests.factory import create_result as create_metaphlan2
from analysis_packages.metaphlan2_data import Metaphlan2ResultModule

from ..models import TopTaxaResult

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
            'taxa_1': random(),
            'taxa_2': random(),
            'taxa_3': random(),
        },
        'prevalence': {
            'taxa_1': random(),
            'taxa_2': random(),
            'taxa_3': random(),
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
