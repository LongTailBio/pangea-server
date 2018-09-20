# pylint: disable=too-few-public-methods

"""Models shared by multiple AnalysisModules."""

from mongoengine import ValidationError, EmbeddedDocument, FloatField


class ModuleResult(EmbeddedDocument):
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


class DistributionResult(EmbeddedDocument):
    """Distribution for a boxplot."""

    min_val = FloatField(required=True)
    q1_val = FloatField(required=True)
    mean_val = FloatField(required=True)
    q3_val = FloatField(required=True)
    max_val = FloatField(required=True)

    def clean(self):
        """Ensure distribution is ordered."""
        values = [self.min_val, self.q1_val, self.mean_val,
                  self.q3_val, self.max_val]
        sorted_values = sorted(values)
        for value, sorted_value in zip(values, sorted_values):
            if value != sorted_value:
                raise ValidationError('Distribution is not in order.')
