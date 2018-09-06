"""Gather all installed ToolResult packages."""

import pkgutil

import tool_packages
from tool_packages.base import SampleToolResultModule, GroupToolResultModule
from tool_packages.base.utils import get_result_module


def discover_local_packages():
    """Construct list of local ToolResult packages."""
    package = tool_packages
    path = package.__path__
    prefix = f'{package.__name__}.'

    results = []
    for _, modname, _ in pkgutil.iter_modules(path, prefix):
        if modname != 'tool_packages.base':
            # Pass dummy value to fromlist in order to import all module members
            module = __import__(modname, fromlist='dummy')
            results.append(module)

    return results


# pylint:disable=invalid-name

all_tool_packages = discover_local_packages()


all_tool_results = [get_result_module(module) for module in all_tool_packages]


all_group_results = [tool for tool in all_tool_results
                     if issubclass(tool, GroupToolResultModule)]


all_sample_results = [tool for tool in all_tool_results
                      if issubclass(tool, SampleToolResultModule)]
