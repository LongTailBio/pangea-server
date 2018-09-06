"""Test suite for Macrobe display module."""

from tool_packages.macrobes import MacrobeResultModule
from tool_packages.macrobes.tests.factory import create_result as create_macrobe

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.macrobes import MacrobeDisplayModule
from app.samples.sample_models import Sample
from app.display_modules.macrobes.models import MacrobeResult
from app.display_modules.macrobes.constants import MODULE_NAME

from .factory import MacrobeFactory, create_one_sample


class TestMacrobeModule(BaseDisplayModuleTest):
    """Test suite for Macrobe diplay module."""

    def test_get_macrobes(self):
        """Ensure getting a single Macrobe behaves correctly."""
        macrobes = MacrobeFactory()
        self.generic_getter_test(macrobes, MODULE_NAME)

    def test_add_macrobes(self):
        """Ensure Macrobe model is created correctly."""
        samples = {
            'sample_1': create_one_sample(),
            'sample_2': create_one_sample(),
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
                                    MacrobeDisplayModule)
