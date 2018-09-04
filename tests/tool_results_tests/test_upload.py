"""Test suite for ToolResult modules API endpoints."""

from app.tool_results.wrangler import all_tool_results

from tool_packages.base import SampleToolResultModule
from tool_packages.base.tests import get_result_module

from .base import BaseToolResultTest


class TestToolResultUploads(BaseToolResultTest):
    """Test suite for ToolResult uploads."""

    pass


for tool_result in all_tool_results:
    base_name = tool_result.__name__
    result_module = get_result_module(tool_result)
    module_name = result_module.name()
    current_factory = __import__(f'{base_name}.tests.factory', fromlist='dummy')

    def add_module(self, module=result_module, name=module_name, factory=current_factory):
        """Ensure a ToolResult model is created correctly."""
        result = factory.create_result(save=False)
        if issubclass(module, (SampleToolResultModule,)):
            self.generic_add_sample_tool_test(result, name)
        else:
            self.generic_add_group_tool_test(result, module.result_model())

    add_module.__doc__ = f'Ensure a raw {tool_result.__name__} model is created correctly.'
    setattr(TestToolResultUploads, f'test_add_{module_name}', add_module)

    def upload_module(self, module=result_module, name=module_name, factory=current_factory):
        """Ensure a raw ToolResult can be uploaded."""
        payload = factory.create_values()
        if issubclass(module, (SampleToolResultModule,)):
            self.generic_test_upload_sample(payload, name)
        else:
            self.generic_test_upload_group(module.result_model(), payload, name)

    upload_module.__doc__ = f'Ensure a raw {tool_result.__name__} can be uploaded.'
    setattr(TestToolResultUploads, f'test_upload_{module_name}', upload_module)
