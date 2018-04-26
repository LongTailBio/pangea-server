"""Test suite for HMP Sites tool result uploads."""

from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest
from app.tool_results.hmp_sites.constants import MODULE_NAME

from .factory import create_values


class TestHmpSitesUploads(BaseToolResultTest):
    """Test suite for HMP Sites tool result uploads."""

    def test_upload_hmp_sites(self):
        """Ensure a raw HMP Sites tool result can be uploaded."""
        payload = create_values()
        self.generic_test_upload_sample(payload, MODULE_NAME)
