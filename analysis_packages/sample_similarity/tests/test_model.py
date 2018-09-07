"""Test suite for Sample Similarity model."""

from unittest import TestCase

from mongoengine import ValidationError

from ..models import SampleSimilarityResult
from .factory import CATEGORIES, TOOLS, DATA_RECORDS


class TestSampleSimilarityModels(TestCase):
    """Test suite for Sample Similarity model."""

    def test_add_sample_similarity(self):
        """Ensure Sample Similarity model is created correctly."""
        sample_similarity_result = SampleSimilarityResult(categories=CATEGORIES,
                                                          tools=TOOLS,
                                                          data_records=DATA_RECORDS)
        try:
            sample_similarity_result.validate()
        except ValidationError:
            self.fail('SampleSimilarityResult validation raised unexpected ValidationError.')

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
        self.assertRaises(ValidationError, sample_similarity_result.validate)

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
        self.assertRaises(ValidationError, sample_similarity_result.validate)

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
        self.assertRaises(ValidationError, sample_similarity_result.validate)

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
        self.assertRaises(ValidationError, sample_similarity_result.validate)
