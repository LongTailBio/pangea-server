"""Test suite for Library module."""

import json
from io import BytesIO

from app.extensions import db

from tests.base import BaseTestCase
from tests.utils import add_sample, add_sample_group, with_user


class TestLibraryModule(BaseTestCase):
    """Test suite for Library module."""

    @with_user
    def test_upload_metadata(self, auth_headers, *_):
        """Ensure metadata spreadsheet may be uploaded for a library."""
        library = add_sample_group(name='Library00')
        sample00 = add_sample(name='sample_00', library_uuid=library.id)
        sample01 = add_sample(name='sample_01', library_uuid=library.id)
        library.samples = [sample00, sample01]
        db.session.commit()

        metadata = (b'sample_name,time,location\n'
                    b'sample_00,morning,turnstile\n'
                    b'sample_01,evening,bench')
        data = dict(metadata=(BytesIO(metadata), 'metadata.csv'))
        endpoint = f'/api/v1/libraries/{library.id}/metadata'
        with self.client:
            response = self.client.post(endpoint,
                                        headers=auth_headers,
                                        data=data,
                                        content_type='multipart/form-data')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertEqual(len(data['data']['updated_uuids']), 2)
