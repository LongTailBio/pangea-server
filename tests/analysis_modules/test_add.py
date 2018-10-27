"""Test suite for adding AnalysisModules."""

from app.analysis_modules.wrangler import all_analysis_modules

from .base import BaseAnalysisModuleTest
from .utils import unpack_module, discover_factory_class


class TestAddAnalysisModule(BaseAnalysisModuleTest):
    """Test suite for adding AnalysisModules."""

    pass


print(all_analysis_modules)
for analysis_module in all_analysis_modules:
    # Grab top-level values we need
    print(analysis_module)
    analysis_name = unpack_module(analysis_module)[1]

    def add_module(self, module=analysis_module):
        """Ensure an AnalysisModules can be added."""
        (_, module_name, factory_module) = unpack_module(module)
        Factory = discover_factory_class(factory_module)  # pylint: disable=invalid-name
        result_model = Factory()
        self.generic_adder_test(result_model, module_name)

    add_module.__doc__ = f'Ensure a {analysis_module.__name__} can be added.'
    setattr(TestAddAnalysisModule, f'test_add_{analysis_name}', add_module)
