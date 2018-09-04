"""Ancestry tool module."""

from mongoengine import ValidationError, MapField, FloatField

from tool_packages.base import SampleToolResultModule
from tool_packages.base.models import ToolResult

from .constants import MODULE_NAME, KNOWN_LOCATIONS


class AncestryToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Ancestry result type."""

    # Dict of form: {<location_id: string>: <percentage: float>}
    populations = MapField(field=FloatField(), required=True)

    def clean(self):
        """Check that all keys are known, all values are [0, 1]."""
        for loc, val in self.populations.items():
            if loc not in KNOWN_LOCATIONS:
                raise ValidationError('No known location: {}'.format(loc))
            if (val > 1) or (val < 0):
                raise ValidationError('Value in bad range.')


class AncestryResultModule(SampleToolResultModule):
    """Ancestry tool module."""

    @classmethod
    def name(cls):
        """Return Ancestry module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return Ancestry module's model class."""
        return AncestryToolResult

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key."""
        return [lambda payload: {'populations': payload}]
