"""Test suite for KrakenHLL tool result uploads."""

import json

from app.samples.sample_models import Sample
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.kraken.tests.constants import TEST_TAXA
from tests.base import BaseTestCase
from tests.utils import with_user


KRAKENHLL_NAME = KrakenHLLResultModule.name()


class TestKrakenHLLUploads(BaseTestCase):
    """Test suite for KrakenHLL tool result uploads."""

    @with_user
    def test_upload_krakenhll(self, auth_headers, *_):
        """Ensure a raw Kraken tool result can be uploaded."""
        sample = Sample(name='SMPL_Krakenhll_01').save()
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/{KRAKENHLL_NAME}',
                headers=auth_headers,
                data=json.dumps(dict(
                    taxa=TEST_TAXA,
                )),
                content_type='application/json',
            )
            rdata = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('taxa', rdata['data'])
            self.assertEqual(rdata['data']['taxa']['d__Viruses'], 1733)
            self.assertIn('success', rdata['status'])

        # Reload object to ensure kraken result was stored properly
        mysample = Sample.objects.get(uuid=sample_uuid)
        self.assertTrue(hasattr(mysample, KRAKENHLL_NAME))
