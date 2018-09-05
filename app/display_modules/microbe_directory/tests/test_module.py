"""Test suite for Microbe Directory diplay module."""

from tool_packages.microbe_directory.tests.factory import (
    create_values,
    create_result as create_microbe_directory,
)

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.microbe_directory import MicrobeDirectoryDisplayModule
from app.samples.sample_models import Sample
from app.display_modules.microbe_directory.models import MicrobeDirectoryResult
from app.display_modules.microbe_directory.constants import MODULE_NAME
from app.display_modules.microbe_directory.tests.factory import MicrobeDirectoryFactory


class TestMicrobeDirectoryModule(BaseDisplayModuleTest):
    """Test suite for Microbe Directory diplay module."""

    def test_get_microbe_directory(self):
        """Ensure getting a single Microbe Directory behaves correctly."""
        microbe_directory = MicrobeDirectoryFactory()
        self.generic_getter_test(microbe_directory, MODULE_NAME)

    def test_add_microbe_directory(self):
        """Ensure Microbe Directory model is created correctly."""
        samples = {
            'sample_1': create_values(),
            'sample_2': create_values(),
        }
        microbe_directory_result = MicrobeDirectoryResult(samples=samples)
        self.generic_adder_test(microbe_directory_result, MODULE_NAME)

    def test_run_microbe_directory_sample_group(self):  # pylint: disable=invalid-name
        """Ensure microbe directory run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_microbe_directory()
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          microbe_directory_annotate=data).save()

        self.generic_run_group_test(create_sample,
                                    MicrobeDirectoryDisplayModule)
