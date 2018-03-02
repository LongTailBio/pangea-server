"""Test suite for Shortbred tool result model."""

from app.samples.sample_models import Sample
from app.tool_results.shortbred import ShortbredResult
from app.tool_results.shortbred.tests.constants import TEST_ABUNDANCES

from tests.base import BaseTestCase


class TestShortbredResultModel(BaseTestCase):
    """Test suite for Shortbred tool result model."""

    def test_add_shortbred_result(self):
        """Ensure Shortbred result model is created correctly."""
        shortbred = ShortbredResult(abundances=TEST_ABUNDANCES)
        sample = Sample(name='SMPL_01', shortbred=shortbred).save()
        self.assertTrue(sample.shortbred)
        tool_result = sample.shortbred
        abundances = tool_result.abundances
        self.assertEqual(len(abundances), 6)
        self.assertEqual(abundances['AAA98484'], 3.996805816740154)
        self.assertEqual(abundances['BAC77251'], 3.6770613514009423)
        self.assertEqual(abundances['TEM_137'], 38.705908962115174)
        self.assertEqual(abundances['YP_002317674'], 4.178478808410161)
        self.assertEqual(abundances['YP_310429'], 10.943634974407566)
        self.assertEqual(abundances['soxR_2'], 5.10702965472353)
