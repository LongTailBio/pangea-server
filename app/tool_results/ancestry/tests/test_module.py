"""Test suite for Ancestry tool result model."""

from app.tool_results.ancestry.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values, create_ancestry


class TestAncestryModel(BaseToolResultTest):
    """Test suite for Ancestry tool result model."""

    def test_add_ancestry(self):
        """Ensure Ancestry tool result model is created correctly."""
        ancestry = create_ancestry()
        self.generic_add_sample_tool_test(ancestry, MODULE_NAME)

    def test_upload_ancestry(self):
        """Ensure a raw Ancestry tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, MODULE_NAME)
