# pylint: disable=too-few-public-methods

"""Base model for Tool Results."""

from mongoengine import Document, UUIDField


class ToolResult(Document):
    """
    Base mongo result class.

    This will be referenced using a ReferenceField or LazyReferenceField.
    """

    # Turns out there isn't much in common between SampleToolResult types...
    meta = {'abstract': True}

    @classmethod
    def scalar_variables(cls):
        """Return a list of all scalar variable names in the class."""
        return []

    @classmethod
    def vector_variables(cls):
        """Return a list of all vector variable names in the class."""
        return []


class GroupToolResult(Document):
    """
    Base mongo group tool result class.

    This will be referenced from a SampleGroup in SQL-land.
    """

    # Sample Group's UUID (SQL-land)
    sample_group_uuid = UUIDField(required=True, binary=False)

    meta = {
        'abstract': True,
        'indexes': [{
            'fields': ['sample_group_uuid'],
            'unique': True,
        }],
    }
