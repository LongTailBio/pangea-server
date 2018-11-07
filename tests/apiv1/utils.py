"""Utilities for APIv1 testing."""

import json

from analysis_packages.ancestry import AncestryAnalysisModule
from analysis_packages.ancestry.tests.factory import create_result as create_ancestry

from app.analysis_results.analysis_result_models import AnalysisResultMeta


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


def get_analysis_result_with_data():
    """Return an analysis result with one anlysis module for groups or samples."""
    analysis_result = AnalysisResultMeta().save()
    analysis_result.set_module_status(AncestryAnalysisModule.name(), 'S')
    result_wrapper = getattr(analysis_result, AncestryAnalysisModule.name()).fetch()
    result_wrapper.data = AncestryAnalysisModule.result_model(**create_ancestry())
    result_wrapper.save()
    analysis_result.save()
    return analysis_result
