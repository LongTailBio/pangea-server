"""Read Stats tool module."""

from mongoengine import IntField, FloatField, MapField

from tool_packages.base import SampleToolResultModule
from tool_packages.base.models import ToolResult


class ReadStatsToolResult(ToolResult):  # pylint: disable=too-few-public-methods
    """A set of consistent fields for read stats."""

    num_reads = IntField()
    gc_content = FloatField()
    codons = MapField(field=IntField(), required=True)
    tetramers = MapField(field=IntField(), required=True)

    @staticmethod
    def stat_fields():
        """Return a list of the stats collected."""
        return ['num_reads', 'gc_content', 'codons', 'tetramers']


class ReadStatsToolResultModule(SampleToolResultModule):
    """Read Stats tool module."""

    @classmethod
    def name(cls):
        """Return Read Stats module's unique identifier string."""
        return 'read_stats'

    @classmethod
    def result_model(cls):
        """Return Read Stats module's model class."""
        return ReadStatsToolResult
