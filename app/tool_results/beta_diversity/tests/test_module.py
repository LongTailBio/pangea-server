"""Test suite for Beta Diversity tool result model."""

from app.tool_results.beta_diversity import BetaDiversityResultModule
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_ranks


class TestBetaDivModel(BaseToolResultTest):
    """Test suite for Beta Div tool result model."""

    def test_add_beta_div(self):
        """Ensure Beta Div tool result model is created correctly."""
        model_cls = BetaDiversityResultModule.result_model()
        beta_diversity = model_cls(data=create_ranks())
        self.generic_add_group_tool_test(beta_diversity, model_cls)

    def test_upload_beta_div(self):
        """Ensure a raw Beta Div tool result can be uploaded."""
        result_cls = BetaDiversityResultModule.result_model()
        payload = {'data': create_ranks()}
        module_name = BetaDiversityResultModule.name()
        self.generic_test_upload_group(result_cls, payload, module_name)
