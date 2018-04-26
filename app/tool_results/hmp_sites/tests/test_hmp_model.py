"""Test suite for HMP Sites tool result model."""

from mongoengine import ValidationError

from app.samples.sample_models import Sample
from app.tool_results.hmp_sites import HmpSitesResult
from app.tool_results.hmp_sites.constants import MODULE_NAME
from app.tool_results.tool_result_test_utils.tool_result_base_test import BaseToolResultTest

from .factory import create_values, create_hmp_sites


class TestHmpSitesModel(BaseToolResultTest):
    """Test suite for HMP Sites tool result model."""

    def test_add_hmp_sites_result(self):
        """Ensure HMP Sites result model is created correctly."""
        hmp_sites = create_hmp_sites()
        self.generic_add_sample_tool_test(hmp_sites, MODULE_NAME)

    def test_add_malformed_hmp_sites_result(self):  # pylint: disable=invalid-name
        """Ensure validation fails for value outside of [0,1]."""
        bad_hmp = dict(create_values())
        bad_hmp['skin'] = [0.5, 1.5]
        hmp_sites = HmpSitesResult(**bad_hmp)
        args = {'name': 'SMPL_01', MODULE_NAME: hmp_sites}
        sample = Sample(**args)
        self.assertRaises(ValidationError, sample.save)
