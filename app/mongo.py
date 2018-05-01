"""Utilities for the mongo within the app."""

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.samples.sample_models import Sample
from app.tool_results import all_tool_results


def drop_mongo_collections():
    """Drop all mongo collections."""
    AnalysisResultMeta.drop_collection()
    Sample.drop_collection()
    for tool_result in all_tool_results:
        tool_result.result_model().drop_collection()
