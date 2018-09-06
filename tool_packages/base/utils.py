"""Utilities for ToolResult packages."""

import inspect

from .modules import BaseToolResultModule


def get_result_module(module):
    """Extract ToolResult result module from package."""
    def test_submodule(submodule):
        """Test a submodule to see if it is a ToolResult module."""
        is_correct_subclass = issubclass(submodule, BaseToolResultModule)
        # Ensure submodule is defined within the package we are inspecting (and not 'base')
        is_correct_module = submodule.__module__ == module.__name__
        return is_correct_subclass and is_correct_module

    submodules = inspect.getmembers(module, inspect.isclass)
    return next(submodule for _, submodule in submodules
                if test_submodule(submodule))
