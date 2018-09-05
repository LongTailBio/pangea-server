"""Test suite for ToolResult modules API endpoints."""

from app.tool_results.wrangler import all_tool_results

from tool_packages.base import SampleToolResultModule

from .base import BaseToolResultTest
from .utils import unpack_package


class TestToolResultUploads(BaseToolResultTest):
    """Test suite for ToolResult uploads."""

    pass


for tool_result in all_tool_results:
    # Grab top-level values we need
    tool_name = unpack_package(tool_result)[2]

    def upload_module(self, package=tool_result):
        """Ensure a raw ToolResult can be uploaded."""
        (base_name, module, module_name, factory) = unpack_package(package)
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

    upload_module.__doc__ = f'Ensure a raw {tool_result.__name__} can be uploaded.'
    setattr(TestToolResultUploads, f'test_upload_{tool_name}', upload_module)
