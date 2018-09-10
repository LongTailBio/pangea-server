"""Average Genome Size Module."""

from analysis_packages.base import AnalysisModule
from tool_packages.microbe_census import MicrobeCensusResultModule

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
    def required_tool_results():
        """List requires ToolResult modules."""
        return [MicrobeCensusResultModule]

    @staticmethod
    def sample_processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
