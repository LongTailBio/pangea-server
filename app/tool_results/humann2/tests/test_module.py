"""Test suite for Humann2 tool result model."""

from app.tool_results.humann2 import Humann2Result
from app.tool_results.humann2.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestHumann2Model(BaseToolResultTest):
    """Test suite for Humann2 tool result model."""

    def test_add_humann2(self):
        """Ensure Humann2 tool result model is created correctly."""
        humann2 = Humann2Result(**create_values())
        self.generic_add_sample_tool_test(humann2, MODULE_NAME)

    def test_upload_humann2(self):
        """Ensure a raw Humann2 tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, MODULE_NAME)
