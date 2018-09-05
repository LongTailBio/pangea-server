"""Test suite for VFDB diplay module."""

from tool_packages.vfdb.tests.factory import create_result as create_vfdb

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.virulence_factors import VirulenceFactorsDisplayModule
from app.samples.sample_models import Sample
from app.display_modules.virulence_factors import VFDBResult
from app.display_modules.virulence_factors.constants import MODULE_NAME
from app.display_modules.virulence_factors.tests.factory import VFDBFactory
from app.display_modules.generic_gene_set.tests.factory import create_one_sample


class TestVFDBModule(BaseDisplayModuleTest):
    """Test suite for VFDB diplay module."""

    def test_get_vfdb(self):
        """Ensure getting a single VFDB behaves correctly."""
        vfdbs = VFDBFactory()
        self.generic_getter_test(vfdbs, MODULE_NAME)

    def test_add_vfdb(self):
        """Ensure VFDB model is created correctly."""
        samples = {
            'test_sample_1': create_one_sample(),
            'test_sample_2': create_one_sample()
        }
        vfdb_result = VFDBResult(samples=samples)
        self.generic_adder_test(vfdb_result, MODULE_NAME)

    def test_run_vfdb_sample_group(self):  # pylint: disable=invalid-name
        """Ensure VFDB run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          vfdb_quantify=create_vfdb()).save()

        self.generic_run_group_test(create_sample,
                                    VirulenceFactorsDisplayModule)
