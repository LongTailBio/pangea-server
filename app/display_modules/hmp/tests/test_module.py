"""Test suite for HMP model."""

from mongoengine import ValidationError

from tool_packages.hmp_sites.tests.factory import create_result as create_hmp_sites

from app.analysis_results.analysis_result_models import AnalysisResultWrapper
from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.hmp import HMPDisplayModule
from app.samples.sample_models import Sample
from app.display_modules.hmp.models import HMPResult
from app.display_modules.hmp.constants import MODULE_NAME
from app.display_modules.hmp.tests.factory import HMPFactory

from .factory import (
    HMPFactory,
    fake_categories,
    fake_sites
)


class TestHMPResult(BaseDisplayModuleTest):
    """Test suite for HMP model."""

    def test_get_hmp(self):
        """Ensure getting a single HMP behaves correctly."""
        hmp = HMPFactory()
        self.generic_getter_test(hmp, MODULE_NAME,
                                 verify_fields=['categories', 'sites', 'data'])

    def test_add_hmp(self):
        """Ensure HMP model is created correctly."""
        hmp = HMPFactory()
        self.generic_adder_test(hmp, MODULE_NAME)

    def test_add_missing_category(self):
        """Ensure saving model fails if category is missing from `data`."""
        hmp = HMPResult(categories=fake_categories(),
                        sites=fake_sites(),
                        data={})
        wrapper = AnalysisResultWrapper(data=hmp)
        self.assertRaises(ValidationError, wrapper.save)

    def test_run_hmp_sample_group(self):  # pylint: disable=invalid-name
        """Ensure hmp run_sample_group produces correct results."""

        def create_sample(i):
            """Create unique sample for index i."""
            data = create_hmp_sites()
            return Sample(name=f'Sample{i}',
                          metadata={'foobar': f'baz{i}'},
                          hmp_site_dists=data).save()

        self.generic_run_group_test(create_sample,
                                    HMPDisplayModule)
