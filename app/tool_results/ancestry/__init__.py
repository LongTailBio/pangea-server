"""Ancestry tool module."""

from mongoengine import ValidationError

from app.extensions import mongoDB
from app.tool_results.modules import SampleToolResultModule
from app.tool_results.models import ToolResult

from .constants import MODULE_NAME, KNOWN_LOCATIONS


class AncestryToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """Ancestry result type."""

    # Dict of form: {<location_id: string>: <percentage: float>}
    populations = mongoDB.MapField(field=mongoDB.FloatField(), required=True)

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
