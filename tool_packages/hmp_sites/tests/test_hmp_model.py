"""Test suite for HMP Sites tool result model."""

from unittest import TestCase

from mongoengine import ValidationError

from tool_packages.hmp_sites import HmpSitesResult
from tool_packages.hmp_sites.constants import MODULE_NAME

from .factory import create_values


class TestHmpSitesModel(TestCase):

    def test_add_malformed_hmp_sites_result(self):  # pylint: disable=invalid-name
        """Ensure validation fails for value outside of [0,1]."""
        bad_hmp = dict(create_values())
        bad_hmp['skin'] = [0.5, 1.5]
        hmp_sites = HmpSitesResult(**bad_hmp)
        self.assertRaises(ValidationError, hmp_sites.validate)
