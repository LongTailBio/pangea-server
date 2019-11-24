"""Test suite for Library module."""

import json
from io import BytesIO

from app.extensions import db

from ..base import BaseTestCase
from ..utils import add_sample, add_sample_group, with_user


class TestLibraryModule(BaseTestCase):
    """Test suite for Library module."""

    @with_user
    def test_upload_metadata(self, auth_headers, *_):
        """Ensure metadata spreadsheet may be uploaded for a library."""
        library = add_sample_group(name='Library00')
        sample00, sample01 = library.sample('sample_00'), library.sample('sample_00')

        metadata = (b'sample_name,time,location\n'
                    b'sample_00,morning,turnstile\n'
                    b'sample_01,evening,bench')
        with self.client:
            response = self.client.post(
                f'/api/v1/libraries/{library.uuid}/metadata',
                headers=auth_headers,
                data=dict(metadata=(BytesIO(metadata), 'metadata.csv')),
                content_type='multipart/form-data'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['updated_uuids']), 2)
