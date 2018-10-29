"""Metaphlan 2 tool module."""

from mongoengine import MapField, IntField, EmbeddedDocument


class Metaphlan2Result(EmbeddedDocument):     # pylint: disable=too-few-public-methods
    """Metaphlan 2 tool's result type."""

    # Taxa is of the form: {<taxon_name>: <abundance_value>}
    taxa = MapField(IntField(), required=True)

    @classmethod
    def vector_variables(cls):
        """Return names of vector variables."""
        return ['taxa']
