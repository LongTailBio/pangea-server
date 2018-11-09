# pylint: disable=invalid-name

"""MetaGenScope seed data from ARBF 2017."""

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper

from .loader import (
    load_sample_similarity,
    load_ags,
)

def create_abrf_analysis_result(save=False):
    """Generate ABRF analysis result."""
    sample_similarity = AnalysisResultWrapper(status='S', data=load_sample_similarity()).save()
    ags = AnalysisResultWrapper(status='S', data=load_ags()).save()
    analysis_result = AnalysisResultMeta(sample_similarity=sample_similarity,
                                         average_genome_size=ags)
    if save:
        analysis_result.save()
    return analysis_result
