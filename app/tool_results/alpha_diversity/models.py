# pylint: disable=too-few-public-methods

"""Alpha Diversity tool module."""

from app.extensions import mongoDB
from app.tool_results.models import ToolResult


class AlphaDiversityToolResult(ToolResult):
    """Alpha Diversity result type."""

    # Accept any JSON
    metaphlan2 = mongoDB.DynamicField(required=True)
    kraken = mongoDB.DynamicField(required=True)

    @staticmethod
    def metrics():
        """Define static metrics for Alpha Diversity tool result."""
        return {
            'metaphlan2': (
                set(['richness', 'shannon_index', 'gini-simpson']),
                'all_reads',
            ), 'kraken': (
                set(['richness', 'shannon_index', 'gini-simpson', 'chao1']),
                '100000',
            )
        }

    @staticmethod
    def tool_names():
        """Return names of available tools."""
        return set(['metaphlan2', 'kraken'])

    @staticmethod
    def taxa_ranks():
        """Return names of available taxa levels."""
        return set(['species', 'genus'])
