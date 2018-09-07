"""Functional Genes module."""

from analysis_packages.base import SampleToolAnalysisModule
from analysis_packages.generic_gene_set.analysis import make_gene_processor
from tool_packages.humann2_normalize import Humann2NormalizeResultModule

from .constants import MODULE_NAME, SOURCE_TOOL_NAME, TOP_N
from .models import FunctionalGenesResult


class FunctionalGenesAnalysisModule(SampleToolAnalysisModule):
    """Functional Genes module."""

    @staticmethod
    def name():
        """Return the name of the module."""
        return MODULE_NAME

    @staticmethod
    def result_model():
        """Return the embedded result."""
        return FunctionalGenesResult

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [Humann2NormalizeResultModule]

    @staticmethod
    def processor():
        """Return the wrangler class."""
        return make_gene_processor(SOURCE_TOOL_NAME, TOP_N)
