"""CARD Genes AnalysisModule."""

from analysis_packages.base import AnalysisModule
from analysis_packages.generic_gene_set.analysis import make_gene_processor
from analysis_packages.card_amrs_data import CARDAMRResultModule

from .constants import MODULE_NAME, SOURCE_TOOL_NAME, TOP_N
from .models import CARDGenesResult


PROCESSOR = make_gene_processor(SOURCE_TOOL_NAME, TOP_N)


class CARDGenesAnalysisModule(AnalysisModule):
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
    def required_modules():
        """Return a list of the necessary result modules."""
        return [CARDAMRResultModule]

    @staticmethod
    def single_sample_processor():
        """Return function(sample_data) for proccessing CARD sample data."""
        return PROCESSOR

    @staticmethod
    def samples_processor():
        """Return function(sample_data) for proccessing CARD sample data."""
        return PROCESSOR
