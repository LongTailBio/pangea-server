"""CARD Genes AnalysisModule."""

from analysis_packages.base import SampleToolAnalysisModule
from tool_packages.card_amrs import CARDAMRResultModule

from .analysis import processor
from .models import CARDGenesResult
from .constants import MODULE_NAME


class CARDGenesAnalysisModule(SampleToolAnalysisModule):
    """CARD Genes factors AnalyisModule."""

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return CARDGenesResult

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [CARDAMRResultModule]

    @staticmethod
    def processor():
        """Return function(*sample_data) for proccessing sample data."""
        return processor
