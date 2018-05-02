"""Test suite for Sample Similarity model."""

from mongoengine import ValidationError

from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.sample_similarity import SampleSimilarityResult
from app.display_modules.sample_similarity.tests.factory import (
    CATEGORIES, TOOLS, DATA_RECORDS

)
from tests.base import BaseTestCase


class TestSampleSimilarityResult(BaseTestCase):
    """Test suite for Sample Similarity model."""

    def test_add_sample_similarity(self):
        """Ensure Sample Similarity model is created correctly."""
        sample_similarity_result = SampleSimilarityResult(categories=CATEGORIES,
                                                          tools=TOOLS,
                                                          data_records=DATA_RECORDS)
        wrapper = AnalysisResultWrapper(data=sample_similarity_result).save()
        result = AnalysisResultMeta(sample_similarity=wrapper).save()
        self.assertTrue(result.id)
        self.assertTrue(result.sample_similarity)

    def test_add_missing_category(self):
        """Ensure saving model fails if sample similarity record is missing category."""
        categories = {
            'city': ['Montevideo', 'Sacramento'],
        }
        data_records = [{
            'SampleID': 'MetaSUB_Pilot__01_cZ__unknown__seq1end',
        }]
        sample_similarity_result = SampleSimilarityResult(categories=categories,
                                                          tools={},
                                                          data_records=data_records)
        wrapper = AnalysisResultWrapper(data=sample_similarity_result)
        self.assertRaises(ValidationError, wrapper.save)

    def test_add_malformed_tool(self):
        """Ensure saving model fails if sample similarity tool is malformed."""
        tools = {
            'metaphlan2': {
                'x_label': 'metaphlan2 tsne x',
            }
        }

        data_records = [{
            'SampleID': 'MetaSUB_Pilot__01_cZ__unknown__seq1end',
            'metaphlan2_x': 0.15631940943278633,
        }]

        sample_similarity_result = SampleSimilarityResult(categories={},
                                                          tools=tools,
                                                          data_records=data_records)
        wrapper = AnalysisResultWrapper(data=sample_similarity_result)
        self.assertRaises(ValidationError, wrapper.save)

    def test_add_missing_tool_x_value(self):
        """Ensure saving model fails if sample similarity record is missing x value."""
        tools = {
            'metaphlan2': {
                'x_label': 'metaphlan2 tsne x',
                'y_label': 'metaphlan2 tsne y'
            }
        }

        data_records = [{
            'SampleID': 'MetaSUB_Pilot__01_cZ__unknown__seq1end',
            'metaphlan2_y': 0.15631940943278633,
        }]

        sample_similarity_result = SampleSimilarityResult(categories={},
                                                          tools=tools,
                                                          data_records=data_records)
        wrapper = AnalysisResultWrapper(data=sample_similarity_result)
        self.assertRaises(ValidationError, wrapper.save)

    def test_add_missing_tool_y_value(self):
        """Ensure saving model fails if sample similarity record is missing y value."""

        tools = {
            'metaphlan2': {
                'x_label': 'metaphlan2 tsne x',
                'y_label': 'metaphlan2 tsne y'
            }
        }

        data_records = [{
            'SampleID': 'MetaSUB_Pilot__01_cZ__unknown__seq1end',
            'metaphlan2_x': 0.15631940943278633,
        }]

        sample_similarity_result = SampleSimilarityResult(categories={},
                                                          tools=tools,
                                                          data_records=data_records)
        wrapper = AnalysisResultWrapper(data=sample_similarity_result)
        self.assertRaises(ValidationError, wrapper.save)
