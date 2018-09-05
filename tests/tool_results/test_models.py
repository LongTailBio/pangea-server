"""Test suite for ToolResult modules API endpoints."""

from app.tool_results.wrangler import all_tool_results

from tool_packages.base import SampleToolResultModule

from .base import BaseToolResultTest
from .utils import unpack_package


class TestToolResultModels(BaseToolResultTest):
    """Test suite for ToolResult uploads."""

    pass


for tool_result in all_tool_results:
    # Grab top-level values we need
    tool_name = unpack_package(tool_result)[2]

    def add_module(self, package=tool_result):
        """Ensure a ToolResult model is created correctly."""
        (_, module, module_name, factory) = unpack_package(package)

        result = factory.create_result(save=False)
        if issubclass(module, (SampleToolResultModule,)):
            self.generic_add_sample_tool_test(result, module_name)
        else:
            self.generic_add_group_tool_test(result, module.result_model())

    add_module.__doc__ = f'Ensure a raw {tool_result.__name__} model is created correctly.'
    setattr(TestToolResultUploads, f'test_add_{tool_name}', add_module)
