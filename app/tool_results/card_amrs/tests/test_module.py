"""Test suite for CARD AMR tool result model."""

from app.tool_results.card_amrs import CARDAMRToolResult
from app.tool_results.card_amrs.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values


class TestCARDAMRModel(BaseToolResultTest):
    """Test suite for CARD AMR tool result model."""

    def test_add_card_amr(self):
        """Ensure CARD AMR tool result model is created correctly."""
        card_amrs = CARDAMRToolResult(**create_values())
        self.generic_add_sample_tool_test(card_amrs, MODULE_NAME)

    def test_upload_card_amr(self):
        """Ensure a raw Methyl tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, MODULE_NAME)
