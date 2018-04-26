"""Test suite for Read Stats tool result model."""

from app.tool_results.read_stats import ReadStatsToolResult
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestReadStatsModel(BaseToolResultTest):
    """Test suite for ReadStats tool result model."""

    def test_add_read_stats(self):
        """Ensure ReadStats tool result model is created correctly."""
        read_stats = ReadStatsToolResult(**create_values())
        self.generic_add_sample_tool_test(read_stats, 'read_stats')

    def test_upload_read_stats(self):
        """Ensure a raw Methyl tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, 'read_stats')
