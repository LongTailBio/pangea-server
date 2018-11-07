"""Average Genome Size Module."""

from analysis_packages.base import AnalysisModule
from analysis_packages.microbe_census_data import MicrobeCensusResultModule

# Re-export modules
from .analysis import processor
from .models import AGSResult
from .constants import MODULE_NAME


class AGSAnalysisModule(AnalysisModule):
    """AGS display module."""

    @staticmethod
    def name():
        """Return unique id string."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return data model class for Average Genome Size type."""
        return AGSResult

    @staticmethod
    def required_modules():
        """List requires ToolResult modules."""
        return [MicrobeCensusResultModule]

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing AGS sample data."""
        return processor
