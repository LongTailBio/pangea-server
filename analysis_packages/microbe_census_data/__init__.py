"""Microbe Census tool module."""

from mongoengine import ValidationError, FloatField, IntField

from analysis_packages.base import AnalysisModule
from analysis_packages.base.models import ModuleResult


class MicrobeCensusResult(ModuleResult):  # pylint: disable=too-few-public-methods
    """Mic Census tool's result type."""

    average_genome_size = FloatField(required=True)
    total_bases = IntField(required=True)
    genome_equivalents = FloatField(required=True)

    def clean(self):
        """Check all values are non-negative, if not raise an error."""
        def validate(*vals):
            """Check vals are non-negative, return a bool."""
            for val in vals:
                if val is not None and val < 0:
                    return False
            return True

        if not validate(self.average_genome_size,
                        self.total_bases,
                        self.genome_equivalents):
            msg = 'MicrobeCensusResult values must be non-negative'
            raise ValidationError(msg)

    @classmethod
    def scalar_variables(cls):
        """Return names of scalar variables."""
        return ['average_genome_size', 'genome_equivalents']


class MicrobeCensusResultModule(AnalysisModule):
    """Microbe Census tool module."""

    @classmethod
    def name(cls):
        """Return Microbe Census module's unique identifier string."""
        return 'microbe_census'

    @classmethod
    def result_model(cls):
        """Return Microbe Census module's model class."""
        return MicrobeCensusResult
