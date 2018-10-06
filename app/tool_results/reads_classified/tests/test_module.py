"""Test suite for Reads Classified tool result model."""

from app.tool_results.reads_classified import ReadsClassifiedToolResult
from app.tool_results.reads_classified.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestReadsClassifiedModel(BaseToolResultTest):
    """Test suite for ReadsClassified tool result model."""

    def test_add_read_stats(self):
        """Ensure ReadsClassified tool result model is created correctly."""
        read_stats = ReadsClassifiedToolResult(**create_values())
        self.generic_add_sample_tool_test(read_stats, MODULE_NAME)

    def test_upload_read_stats(self):
        """Ensure a raw ReadsClassified tool result can be uploaded."""
        payload = {'proportions': create_values()}
        self.generic_test_upload_sample(payload, MODULE_NAME)
