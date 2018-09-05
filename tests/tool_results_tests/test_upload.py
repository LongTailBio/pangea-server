"""Test suite for ToolResult modules API endpoints."""

from app.tool_results.wrangler import all_tool_results

from tool_packages.base import SampleToolResultModule
from tool_packages.base.tests import get_result_module

from .base import BaseToolResultTest


class TestToolResultUploads(BaseToolResultTest):
    """Test suite for ToolResult uploads."""

    pass


def unpack_package(package):
    """Unpack a module class into useful parts."""
    base_name = package.__name__
    result_module = get_result_module(package)
    module_name = result_module.name()
    factory = __import__(f'{base_name}.tests.factory', fromlist='dummy')
    return (base_name, result_module, module_name, factory)


for tool_result in all_tool_results:
    # Grab top-level values we need
    tool_name = unpack_package(tool_result)[2]

    def add_module(self, package=tool_result):
        """Ensure a ToolResult model is created correctly."""
        (base_name, module, module_name, factory) = unpack_package(package)

        result = factory.create_result(save=False)
        if issubclass(module, (SampleToolResultModule,)):
            self.generic_add_sample_tool_test(result, module_name)
        else:
            self.generic_add_group_tool_test(result, module.result_model())

    add_module.__doc__ = f'Ensure a raw {tool_result.__name__} model is created correctly.'
    setattr(TestToolResultUploads, f'test_add_{tool_name}', add_module)

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
