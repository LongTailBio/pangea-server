"""Test suite for ToolResult modules API endpoints."""

from app.tool_results.wrangler import all_tool_results
from tool_packages.base.tests import get_result_module

from .base import BaseToolResultTest


class TestToolResultUploads(BaseToolResultTest):
    """Test suite for ToolResult uploads."""

    pass


for tool_result in all_tool_results:
    module = tool_result
    base_name = module.__name__
    result_module = get_result_module(module)
    module_name = result_module.name()
    current_factory = __import__(f'{base_name}.tests.factory', fromlist='dummy')

    def add_module(self, name=module_name, factory=current_factory):
        """Ensure a ToolResult model is created correctly."""
        result = factory.create_result()
        self.generic_add_sample_tool_test(result, name)

    setattr(TestToolResultUploads, f'test_add_{module_name}', add_module)

    def upload_module(self, name=module_name, factory=current_factory):
        """Ensure a raw ToolResult can be uploaded."""
        payload = factory.create_values()
        self.generic_test_upload_sample(payload, name)

    setattr(TestToolResultUploads, f'test_upload_{module_name}', upload_module)
