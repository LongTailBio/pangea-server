"""Test suite for Query Result model."""

from mongoengine import ValidationError

from app.query_results.query_result_models import QueryResult, SampleSimilarityResult
from tests.base import BaseTestCase


class TestSampleSimilarityResult(BaseTestCase):
    """Test suite for Query Result model."""

    def test_add_sample_similarity(self):
        """Ensure organization model is created correctly."""

        categories = {
            'city': ['Montevideo', 'Sacramento']
        }

        tools = {
            'metaphlan2': {
                'x_label': 'metaphlan2 tsne x',
                'y_label': 'metaphlan2 tsne y'
            }
        }

        data_records = [{
            'SampleID': 'MetaSUB_Pilot__01_cZ__unknown__seq1end',
            'city': 'Montevideo',
            'metaphlan2_x': 0.46118640628005614,
            'metaphlan2_y': 0.15631940943278633,
        }]

        sample_similarity_result = SampleSimilarityResult(categories=categories,
                                                          tools=tools,
                                                          data_records=data_records)
        result = QueryResult(sample_similarity=sample_similarity_result).save()
        self.assertTrue(result.id)
        self.assertTrue(result.sample_similarity)

    def test_add_missing_category(self):
        """Ensure saving model fails if sample similarity record is missing category."""

        categories = {
            'city': ['Montevideo', 'Sacramento']
        }

        data_records = [{
            'SampleID': 'MetaSUB_Pilot__01_cZ__unknown__seq1end',
        }]

        sample_similarity_result = SampleSimilarityResult(categories=categories,
                                                          tools={},
                                                          data_records=data_records)
        result = QueryResult(sample_similarity=sample_similarity_result)
        self.assertRaises(ValidationError, result.save)

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
        result = QueryResult(sample_similarity=sample_similarity_result)
        self.assertRaises(ValidationError, result.save)

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
        result = QueryResult(sample_similarity=sample_similarity_result)
        self.assertRaises(ValidationError, result.save)

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
        result = QueryResult(sample_similarity=sample_similarity_result)
        self.assertRaises(ValidationError, result.save)