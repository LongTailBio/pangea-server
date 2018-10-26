"""Functional Genes module."""

from analysis_packages.base import AnalysisModule
from analysis_packages.generic_gene_set.analysis import make_gene_processor
from analysis_packages.humann2_normalize_data import Humann2NormalizeResultModule

from .constants import MODULE_NAME, SOURCE_TOOL_NAME, TOP_N
from .models import FunctionalGenesResult


PROCESSOR = make_gene_processor(SOURCE_TOOL_NAME, TOP_N)


class FunctionalGenesAnalysisModule(AnalysisModule):
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
    def required_tool_modules():
        """Return a list of the necessary result modules."""
        return [Humann2NormalizeResultModule]

    @staticmethod
    def single_sample_processor():
        """Return function(sample_data) for proccessing Functional Genes sample data."""
        return PROCESSOR

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing Functional Genes sample data."""
        return PROCESSOR
