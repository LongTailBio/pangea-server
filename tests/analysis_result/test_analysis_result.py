"""Test suite for AnalysisResultMeta model."""

from pangea_modules.ags.constants import MODULE_NAME
from pangea_modules.ags.factory import AGSFactory

from app.db_models import AnalysisResult

from tests.base import BaseTestCase


class TestAnalysisResultMetaModel(BaseTestCase):
    """Test suite for SampleGroup model."""

    def test_result_types(self):
        """Ensure sample group model is created correctly."""
        ags_result = AnalysisResultWrapper(status='S', data=AGSFactory()).save()
        analysis_result = AnalysisResultMeta()
        setattr(analysis_result, MODULE_NAME, ags_result)
        analysis_result.save()
        self.assertEqual(len(analysis_result.result_types), 1)
        self.assertIn(MODULE_NAME, analysis_result.result_types)
