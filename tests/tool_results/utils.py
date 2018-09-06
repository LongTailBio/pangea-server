"""Utilities for testing ToolResults."""


def unpack_module(tool_module):
    """Unpack a module class into useful parts."""
    base_name = tool_module.__module__
    module_name = tool_module.name()
    # Pass dummy value to fromlist in order to import all module members
    factory = __import__(f'{base_name}.tests.factory', fromlist='dummy')
    return (base_name, module_name, factory)
