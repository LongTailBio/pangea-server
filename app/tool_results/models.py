# pylint: disable=too-few-public-methods

"""Base model for Group Tool Results."""

from app.extensions import mongoDB


class ToolResult(mongoDB.EmbeddedDocument):
    """Base mongo result class."""

    # Turns out there isn't much in common between SampleToolResult types...

    meta = {'abstract': True}


# This is a Document (not an EmbeddedDocument) because it is
# attached to a SQL SampleGroup, not nested within a Mongo Sample
class GroupToolResult(mongoDB.Document):
    """Base mongo group tool result class."""

    # Sample Group's UUID (SQL-land)
    sample_group_uuid = mongoDB.UUIDField(required=True, binary=False)

    meta = {'abstract': True}
