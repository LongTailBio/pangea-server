"""Test suite for Methyls diplay module."""
from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.methyls import MethylsDisplayModule
from app.samples.sample_models import Sample
from app.display_modules.methyls import MethylResult
from app.display_modules.methyls.tests.factory import MethylsFactory
from app.display_modules.generic_gene_set.tests.factory import create_one_sample
from app.tool_results.methyltransferases.tests.factory import create_methyls


class TestMethylsModule(BaseDisplayModuleTest):
    """Test suite for Methyls diplay module."""

    def test_get_methyls(self):
        """Ensure getting a single Methyl behaves correctly."""
        methyls = MethylsFactory()
        self.generic_getter_test(methyls, 'methyltransferases')

    def test_add_methyls(self):
        """Ensure Methyl model is created correctly."""
        samples = {
            'test_sample_1': create_one_sample(),
            'test_sample_2': create_one_sample(),
        }
        methyls_result = MethylResult(samples=samples)
        self.generic_adder_test(methyls_result, 'methyltransferases')

    def test_run_methyls_sample_group(self):  # pylint: disable=invalid-name
        """Ensure methyls run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          align_to_methyltransferases=create_methyls()).save()

        self.generic_run_group_test(create_sample,
                                    MethylsDisplayModule)
