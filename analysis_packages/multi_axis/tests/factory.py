# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Multi Axis models for testing."""

import factory

from analysis_packages.card_amrs_data.tests.factory import create_result as create_card_amr
from analysis_packages.humann2_normalize_data.tests.factory import (
    create_result as create_humann2_normalize,
)
from analysis_packages.krakenhll_data.tests.factory import create_result as create_krakenhll
from analysis_packages.metaphlan2_data.tests.factory import create_result as create_metaphlan2
from analysis_packages.microbe_census_data.tests.factory import create_result as create_mc

from ..models import MultiAxisResult


def create_values():
    """Return values used in MultiAxis."""
    return {
        'metaphlan2_taxonomy_profiling': create_metaphlan2(),
        'krakenhll_taxonomy_profiling': create_krakenhll(),
        'align_to_amr_genes': create_card_amr(),
        'humann2_normalize_genes': create_humann2_normalize(),
        'microbe_census': create_mc(),
    }


class MultiAxisFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Microbe Directory."""

    class Meta:
        """Factory metadata."""

        model = MultiAxisResult

    categories = {
        'foo': ['foo_1', 'foo_2'],
        'bar': ['bar_1', 'bar_2'],
    }
    axes = {
        'axis_1': {'vals': {'sample_1': 1, 'sample_2': 2}},
        'axis_2': {'vals': {'sample_1': 3, 'sample_2': 4}},
    }
    metadata = {
        'sample_1': {'foo': 'foo_1', 'bar': 'bar_1'},
        'sample_2': {'foo': 'foo_2', 'bar': 'bar_2'},
    }
