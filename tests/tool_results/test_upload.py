"""Test suite for ToolResult modules API endpoints."""

from app.tool_results.wrangler import all_tool_results

from tool_packages.base import SampleToolResultModule

from .base import BaseToolResultTest
from .utils import unpack_module


class TestToolResultUploads(BaseToolResultTest):
    """Test suite for ToolResult uploads."""

    pass


for tool_module in all_tool_results:
    # Grab top-level values we need
    tool_name = unpack_module(tool_module)[1]

    def upload_module(self, module=tool_module):
        """Ensure a raw ToolResult can be uploaded."""
        (base_name, module_name, factory) = unpack_module(module)
        payload = factory.create_values()
        try:
            path = f'{base_name}.tests.utils'
            util = __import__(path, fromlist=['package_payload'])
            payload = util.package_payload(payload)
        except ModuleNotFoundError:
            pass

        if issubclass(module, (SampleToolResultModule,)):
            self.generic_test_upload_sample(payload, module_name)
        else:
            self.generic_test_upload_group(module.result_model(), payload, module_name)

    upload_module.__doc__ = f'Ensure a raw {tool_module.__name__} can be uploaded.'
    setattr(TestToolResultUploads, f'test_upload_{tool_name}', upload_module)
