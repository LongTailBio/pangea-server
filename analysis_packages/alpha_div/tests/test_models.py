"""Test suite for Alpha Diversity models."""

from unittest import TestCase
from mongoengine import ValidationError

from ..models import AlphaDiversityResult
from .factory import create_categories, create_tools, create_by_tool


class TestAlphaDivModule(TestCase):
    """Test suite for Alpha Diversity diplay module."""

    def test_add_alpha_div(self):
        """Ensure Alpha Diversity model is created correctly."""
        packed_data = {
            'categories': create_categories(),
            'tool_names': create_tools(),
        }
        packed_data['by_tool'] = create_by_tool(packed_data)
        alpha_div_result = AlphaDiversityResult(**packed_data)
        try:
            alpha_div_result.validate()
        except ValidationError:
            self.fail('AlphaDiversityResult validation raised unexpected ValidationError.')
