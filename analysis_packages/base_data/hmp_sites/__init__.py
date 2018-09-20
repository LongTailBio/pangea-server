"""HMP Sites tool module."""

from mongoengine import ValidationError, ListField, FloatField

from analysis_packages.base import AnalysisModule
from analysis_packages.base.models import ModuleResult


from .constants import MODULE_NAME


class HmpSitesResult(ModuleResult):       # pylint: disable=too-few-public-methods
    """HMP Sites tool's result type."""

    # Lists of values for each example microbiome comparison; may not be empty
    skin = ListField(FloatField(), required=True)
    oral = ListField(FloatField(), required=True)
    urogenital_tract = ListField(FloatField(), required=True)
    airways = ListField(FloatField(), required=True)
    gastrointestinal = ListField(FloatField(), required=True)

    def clean(self):
        """Check that all vals are in range [0, 1] if not then error."""
        def validate(*vals):
            """Confirm values are in range [0,1], if they exist."""
            for value_list in vals:
                for value in value_list:
                    if value is not None and (value < 0 or value > 1):
                        return False
            return True

        if not validate(self.skin,
                        self.oral,
                        self.urogenital_tract,
                        self.airways,
                        self.gastrointestinal):
            msg = 'HMPSitesResult values in bad range'
            raise ValidationError(msg)

    @staticmethod
    def site_names():
        """Return the names of the body sites."""
        return ['skin', 'oral', 'urogenital_tract', 'airways', 'gastrointestinal']


class HmpSitesResultModule(AnalysisModule):
    """HMP Sites tool module."""

    @classmethod
    def name(cls):
        """Return HMP Sites module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return HMP Sites module's model class."""
        return HmpSitesResult
