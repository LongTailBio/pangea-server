"""Shortbred tool module."""

from mongoengine import MapField, FloatField

from tool_packages.base import SampleToolResultModule
from tool_packages.base.models import ToolResult


class ShortbredResult(ToolResult):      # pylint: disable=too-few-public-methods
    """Shortbred tool's result type."""

    # Abundances is of the form: {<amr_gene>: <abundance_value>}
    abundances = MapField(FloatField(), required=True)


class ShortbredResultModule(SampleToolResultModule):
    """Shortbred tool module."""

    @classmethod
    def name(cls):
        """Return Shortbred module's unique identifier string."""
        return 'shortbred_amr_profiling'

    @classmethod
    def result_model(cls):
        """Return Shortbred module's model class."""
        return ShortbredResult
