"""Utilities for testing ToolResults."""

from tool_packages.base.utils import get_result_module


def unpack_package(package):
    """Unpack a module class into useful parts."""
    base_name = package.__name__
    result_module = get_result_module(package)
    module_name = result_module.name()
    # Pass dummy value to fromlist in order to import all module members
    factory = __import__(f'{base_name}.tests.factory', fromlist='dummy')
    return (base_name, result_module, module_name, factory)
