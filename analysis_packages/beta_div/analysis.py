"""Tasks to process Beta Diversity results."""

from analysis_packages.base.utils import jsonify


def processor(group_tool_result):
    """Wrap Beta Diversity component calculations."""
    return {'data': jsonify(group_tool_result)['data']}
