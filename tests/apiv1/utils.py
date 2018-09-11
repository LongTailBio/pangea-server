"""Utilities for APIv1 testing."""

import json


def middleware_tester(test_case, auth_headers, mocked_conductor, endpoint):
    """Execute common middleware API testing code."""
    with test_case.client:
        response = test_case.client.post(
            endpoint,
            headers=auth_headers,
            content_type='application/json',
        )
        test_case.assertEqual(response.status_code, 202)
        data = json.loads(response.data.decode())
        test_case.assertIn('middleware', data['data'])
        mocked_conductor.assert_called_once()
