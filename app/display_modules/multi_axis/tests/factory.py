# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Multi Axis models for testing."""

import factory

from app.display_modules.multi_axis import MultiAxisResult
from app.tool_results.card_amrs.tests.factory import create_card_amr
from app.tool_results.humann2_normalize.tests.factory import create_humann2_normalize
from app.tool_results.krakenhll.tests.factory import create_krakenhll
from app.tool_results.metaphlan2.tests.factory import create_metaphlan2
from app.tool_results.microbe_census.tests.factory import create_microbe_census


def create_values():
    """Return values used in MultiAxis."""
    return {
        'metaphlan2_taxonomy_profiling': create_metaphlan2(),
        'krakenhll_taxonomy_profiling': create_krakenhll(),
        'align_to_amr_genes': create_card_amr(),
        'humann2_normalize_genes': create_humann2_normalize(),
        'microbe_census': create_microbe_census(),
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
