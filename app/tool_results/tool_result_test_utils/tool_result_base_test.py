"""Base test suite and utilities for tool result modules."""

import json

from app.samples.sample_models import Sample

from tests.base import BaseTestCase
from tests.utils import add_sample, add_sample_group, get_test_user


class BaseToolResultTest(BaseTestCase):
    """Test suite for VFDB tool result model."""

    def generic_add_sample_tool_test(self, result, tool_result_name):  # pylint: disable=invalid-name
        """Ensure tool result model is created correctly."""
        result.save()
        sample = Sample(name='SMPL_01',
                        **{tool_result_name: result}).save()
        self.assertTrue(getattr(sample, tool_result_name))

    def generic_add_group_tool_test(self, result, model_cls):  # pylint: disable=invalid-name
        """Ensure tool result model is created correctly."""
        sample_group = add_sample_group(name='SMPL_01')
        result.sample_group_uuid = sample_group.id
        result.save()

        fetch_result = model_cls.objects.get(sample_group_uuid=sample_group.id)
        self.assertTrue(fetch_result is not None)

    def help_test_upload(self, endpoint, payload):
        """Ensure a raw tool result can be uploaded."""
        auth_headers, _ = get_test_user(self.client)
        with self.client:
            response = self.client.post(
                endpoint,
                headers=auth_headers,
                data=json.dumps(payload),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            for field in payload:
                self.assertIn(field, data['data'])

    def generic_test_upload_sample(self, payload, tool_result_name):
        """Ensure a raw Sample tool result can be uploaded."""
        metadata = {'category_01': 'value_01'}
        sample = add_sample(name='SMPL_Microbe_Directory_01', metadata=metadata)
        sample_uuid = str(sample.uuid)
        endpoint = f'/api/v1/samples/{sample_uuid}/{tool_result_name}'

        self.help_test_upload(endpoint, payload)

        # Reload object to ensure microbe directory result was stored properly
        sample = Sample.objects.get(uuid=sample_uuid)
        self.assertTrue(getattr(sample, tool_result_name))

    def generic_test_upload_group(self, result_cls, payload, tool_result_name):
        """Ensure a raw Sample Group tool result can be uploaded."""
        sample_group = add_sample_group(name=f'GRP_{tool_result_name}')
        group_uuid = str(sample_group.id)
        endpoint = f'/api/v1/sample_groups/{group_uuid}/{tool_result_name}'

        self.help_test_upload(endpoint, payload)

        # Reload object to ensure tool result was stored properly
        tool_result = result_cls.objects.get(sample_group_uuid=group_uuid)
        self.assertTrue(tool_result)
