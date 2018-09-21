"""Utilities for the mongo within the app."""

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.samples.sample_models import Sample


def drop_mongo_collections():
    """Drop all mongo collections."""
    AnalysisResultMeta.drop_collection()
    Sample.drop_collection()
