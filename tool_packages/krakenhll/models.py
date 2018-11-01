# pylint: disable=too-few-public-methods

"""Models for Kraken tool module."""

from mongoengine import MapField, IntField

from tool_packages.base.models import ToolResult


class KrakenHLLResult(ToolResult):
    """Kraken tool's result type."""

    # Taxa is of the form: {<taxon_name>: <abundance_value>}
    taxa = MapField(IntField(), required=True)

    @classmethod
    def vector_variables(cls):
        """Return names of vector variables."""
        return ['taxa']
