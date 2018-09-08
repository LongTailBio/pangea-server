"""Test suite for AnalysisModules API endpoints."""

import json
from pprint import pprint

from app.analysis_modules.wrangler import all_analysis_modules

from .base import BaseAnalysisModuleTest
from .utils import unpack_module, discover_factory_class


class TestAnalysisModuleUploads(BaseAnalysisModuleTest):
    """Test suite for getting AnalysisModules results."""

    pass


for analysis_module in all_analysis_modules:
    # Grab top-level values we need
    analysis_name = unpack_module(analysis_module)[1]

    def fetch_module(self, module=analysis_module):
        """Ensure an AnalysisModules can be fetched."""
        (base_name, module_name, factory_module) = unpack_module(module)
        Factory = discover_factory_class(factory_module)
        result_model = Factory()
        fields = list(result_model._fields.keys())
        self.generic_getter_test(result_model, module_name, verify_fields=fields)

    fetch_module.__doc__ = f'Ensure a {analysis_module.__name__} can be fetched.'
    setattr(TestAnalysisModuleUploads, f'test_fetch_{analysis_name}', fetch_module)
