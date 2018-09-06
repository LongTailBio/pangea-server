"""Average Genome Size Module."""

from analysis_packages.base import SampleToolAnalysisModule
from tool_packages.microbe_census import MicrobeCensusResultModule

# Re-export modules
from .analysis import processor
from .models import AGSResult
from .constants import MODULE_NAME


class AGSAnalysisModule(SampleToolAnalysisModule):
    """AGS display module."""

    @classmethod
    def name(cls):
        """Return unique id string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return data model class for Average Genome Size type."""
        return AGSResult

    @staticmethod
    def required_tool_results():
        """List requires ToolResult modules."""
        return [MicrobeCensusResultModule]

    @staticmethod
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
