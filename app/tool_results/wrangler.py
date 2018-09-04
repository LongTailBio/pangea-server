"""Gather all installed ToolResult packages."""

import pkgutil

import tool_packages


def discover_local_packages():
    """Construct list of local ToolResult packages."""
    package = tool_packages
    path = package.__path__
    prefix = f'{package.__name__}.'

    results = []
    for _, modname, _ in pkgutil.iter_modules(path, prefix):
        if modname != 'tool_packages.base':
            module = __import__(modname, fromlist='dummy')
            results.append(module)

    return results


all_tool_results = discover_local_packages()  # pylint:disable=invalid-name
