"""Utilities for testing AnalysisModules."""

import inspect

from factory.mongoengine import MongoEngineFactory


def discover_factory_class(factory_module):
    """Extract ToolResult result module from package."""
    def test_submodule(submodule):
        """Test a submodule to see if it is a ToolResult module."""
        is_correct_subclass = issubclass(submodule, MongoEngineFactory)
        # Ensure submodule is defined within the package we are inspecting (and not 'base')
        is_correct_module = factory_module.__name__ in submodule.__module__
        return is_correct_subclass and is_correct_module

    submodules = inspect.getmembers(factory_module, inspect.isclass)
    return next(submodule for _, submodule in submodules
                if test_submodule(submodule))


def unpack_module(analysis_module):
    """Unpack a module class into useful parts."""
    base_name = analysis_module.__module__
    module_name = analysis_module.name()
    # Pass dummy value to fromlist in order to import all module members
    print(base_name)
    root_name = '.'.join(base_name.split('.')[:-1])
    print(root_name)
    factory_module = __import__(f'{root_name}.tests.factory', fromlist='dummy')
    return (base_name, module_name, factory_module)
