"""Test suite for Top Taxa diplay module."""

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.top_taxa import TopTaxaDisplayModule
from app.samples.sample_models import Sample
from app.display_modules.top_taxa.constants import MODULE_NAME

from .factory import TopTaxaFactory, create_values


class TestTopAxisModule(BaseDisplayModuleTest):
    """Test suite for Top Taxa diplay module."""

    def test_get_top_taxa(self):
        """Ensure getting a single TopTaxa behaves correctly."""
        top_taxa = TopTaxaFactory()
        self.generic_getter_test(top_taxa, MODULE_NAME,
                                 verify_fields=['categories'])

    def test_add_top_taxa(self):
        """Ensure TopTaxa model is created correctly."""
        top_taxa = TopTaxaFactory()
        self.generic_adder_test(top_taxa, MODULE_NAME)

    def test_run_top_taxa_sample_group(self):  # pylint: disable=invalid-name
        """Ensure top_taxa run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            return Sample(
                name=f'Sample_{i}',
                metadata={'foobizz': f'bar{i}'},
                **create_values(),
            ).save()

        self.generic_run_group_test(
            create_sample,
            TopTaxaDisplayModule
        )
