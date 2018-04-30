"""Test suite for Reads Classified tool result uploads."""

import json

from app.samples.sample_models import Sample
from app.tool_results.reads_classified import MODULE_NAME
from app.tool_results.reads_classified.tests.constants import TEST_READS

from tests.base import BaseTestCase
from tests.utils import with_user


class TestReadsClassifiedUploads(BaseTestCase):
    """Test suite for Reads Classified tool result uploads."""

    @with_user
    def test_upload_reads_classified(self, auth_headers, *_):
        """Ensure a raw Reads Classified tool result can be uploaded."""
        sample = Sample(name='SMPL_Reads_01').save()
        sample_uuid = str(sample.uuid)
        with self.client:
            response = self.client.post(
                f'/api/v1/samples/{sample_uuid}/{MODULE_NAME}',
                headers=auth_headers,
                data=json.dumps(TEST_READS),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['data']['viral'], 100)
            self.assertEqual(data['data']['archaeal'], 200)
            self.assertEqual(data['data']['bacterial'], 600)
            self.assertEqual(data['data']['host'], 50)
            self.assertEqual(data['data']['unknown'], 50)
            self.assertIn('success', data['status'])

        # Reload object to ensure HMP Sites result was stored properly
        sample = Sample.objects.get(uuid=sample_uuid)
        self.assertTrue(hasattr(sample, MODULE_NAME))
