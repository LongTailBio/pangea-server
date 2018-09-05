"""
DEPRECATED: Food and Pet tool module.

This module is different in the new pipeline and should be ignored for now.
"""

from mongoengine import DictField, IntField

from tool_packages.base import SampleToolResultModule
from tool_packages.base.models import ToolResult


class FoodPetResult(ToolResult):        # pylint: disable=too-few-public-methods
    """Food/Pet tool's result type."""

    # DictFields are of the form: {<sample_id>: <sample_value>}
    vegetables = DictField(default={})
    fruits = DictField(default={})
    pets = DictField(default={})
    meats = DictField(default={})

    total_reads = IntField()


class FoodPetResultModule(SampleToolResultModule):
    """Food and Pet tool module."""

    @classmethod
    def name(cls):
        """Return Food and Pet module's unique identifier string."""
        return 'food_and_pet'

    @classmethod
    def result_model(cls):
        """Return Food and Pet module's model class."""
        return FoodPetResult
