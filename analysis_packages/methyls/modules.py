"""Methyls module."""

from analysis_packages.base import AnalysisModule
from analysis_packages.generic_gene_set.analysis import make_gene_processor
from tool_packages.methyltransferases import MethylResultModule

from .constants import MODULE_NAME, SOURCE_TOOL_NAME, TOP_N
from .models import MethylResult


class MethylsAnalysisModule(AnalysisModule):
    """Methyltransferase AnalysisModule."""

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return MethylResult

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [MethylResultModule]

    @staticmethod
    def sample_processor():
        """Return function(*sample_data) for proccessing sample data."""
        return make_gene_processor(SOURCE_TOOL_NAME, TOP_N)
