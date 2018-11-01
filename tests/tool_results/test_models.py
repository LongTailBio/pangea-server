"""Test suite for ToolResult modules API endpoints."""

from app.tool_results.wrangler import all_tool_results

from tool_packages.base import SampleToolResultModule

from .base import BaseToolResultTest
from .utils import unpack_module


class TestToolResultModels(BaseToolResultTest):
    """Test suite for ToolResult models."""

    pass


for tool_module in all_tool_results:
    # Grab top-level values we need
    tool_name = unpack_module(tool_module)[1]

    def add_module(self, module=tool_module):
        """Ensure a ToolResult model is created correctly."""
        (_, module_name, factory) = unpack_module(module)

        result = factory.create_result(save=False)
        if issubclass(module, (SampleToolResultModule,)):
            self.generic_add_sample_tool_test(result, module_name)
        else:
            self.generic_add_group_tool_test(result, module.result_model())

    add_module.__doc__ = f'Ensure a raw {tool_module.__name__} model is created correctly.'
    setattr(TestToolResultModels, f'test_add_{tool_name}', add_module)
