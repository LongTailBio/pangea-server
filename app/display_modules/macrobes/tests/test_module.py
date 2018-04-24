"""Test suite for Macrobe display module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.macrobe.wrangler import MacrobeWrangler
from app.samples.sample_models import Sample
from app.display_modules.macrobe.models import MacrobeResult
from app.display_modules.macrobe.constants import MODULE_NAME
from app.tool_results.macrobes import MacrobeResultModule
from app.tool_results.macrobes.tests.factory import (
    create_values,
    create_macrobe
)

from .factory import MacrobeFactory


class TestMicrobeDirectoryModule(BaseDisplayModuleTest):
    """Test suite for Macrobe diplay module."""

    def test_get_macrobes(self):
        """Ensure getting a single Macrobe behaves correctly."""
        macrobes = MacrobeFactory()
        self.generic_getter_test(macrobes, MODULE_NAME)

    def test_add_macrobes(self):
        """Ensure Macrobe model is created correctly."""
        samples = {
            'sample_1': create_values(),
            'sample_2': create_values(),
        }
        macrobe_result = MacrobeResult(samples=samples)
        self.generic_adder_test(macrobe_result, MODULE_NAME)

    def test_run_macrobes_sample_group(self):  # pylint: disable=invalid-name
        """Ensure Macrobe run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_macrobe()
            return Sample(**{
                'name': f'Sample{i}',
                'metadata': {'foobar': f'baz{i}'},
                MacrobeResultModule.name(): data
            }).save()

        self.generic_run_group_test(create_sample,
                                    MacrobeWrangler,
                                    MODULE_NAME)
