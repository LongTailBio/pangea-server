"""Test suite for Methyls tool result model."""
from app.tool_results.methyltransferases import MethylToolResult
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestMethylsModel(BaseToolResultTest):
    """Test suite for Methyls tool result model."""

    def test_add_methyls(self):
        """Ensure Methyls tool result model is created correctly."""

        methyls = MethylToolResult(**create_values())
        self.generic_add_sample_tool_test(methyls, 'align_to_methyltransferases')

    def test_upload_methyls(self):
        """Ensure a raw Methyl tool result can be uploaded."""

        payload = create_values()
        self.generic_test_upload_sample(payload, 'align_to_methyltransferases')
