# pylint: disable=too-few-public-methods

"""Models shared by multiple modules."""

from mongoengine import ValidationError

from app.extensions import mongoDB as mdb


class DistributionResult(mdb.EmbeddedDocument):
    """Distribution for a boxplot."""

    min_val = mdb.FloatField(required=True)
    q1_val = mdb.FloatField(required=True)
    mean_val = mdb.FloatField(required=True)
    q3_val = mdb.FloatField(required=True)
    max_val = mdb.FloatField(required=True)

    def clean(self):
        """Ensure distribution is ordered."""
        values = [self.min_val, self.q1_val, self.mean_val,
                  self.q3_val, self.max_val]
        sorted_values = sorted(values)
        for value, sorted_value in zip(values, sorted_values):
            if value != sorted_value:
                raise ValidationError('Distribution is not in order.')
