"""Test suite for Reads Classified display module."""

from random import randint

from app.display_modules.display_module_base_test import BaseDisplayModuleTest
from app.display_modules.volcano import VolcanoDisplayModule
from app.display_modules.volcano.models import VolcanoResult
from app.display_modules.volcano.constants import MODULE_NAME
from app.display_modules.volcano.tests.factory import VolcanoFactory
from app.samples.sample_models import Sample
from app.tool_results.card_amrs import CARDAMRResultModule
from app.tool_results.card_amrs.tests.factory import create_card_amr
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.kraken.tests.factory import create_kraken
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.metaphlan2.tests.factory import create_metaphlan2

from .factory import make_tool_doc


class TestVolcanoModule(BaseDisplayModuleTest):
    """Test suite for Volcano diplay module."""

    def test_get_volcano(self):
        """Ensure getting a single Volcano behaves correctly."""
        reads_class = VolcanoFactory()
        self.generic_getter_test(reads_class, MODULE_NAME,
                                 verify_fields=('categories', 'tools'))

    def test_add_volcano(self):
        """Ensure Volcano model is created correctly."""
        categories = {
            f'cat_name_{i}': [
                f'cat_name_{i}_val_{j}'
                for j in range(randint(3, 6))
            ] for i in range(randint(3, 6))
        }
        tool_names = [f'tool_{i}' for i in range(randint(3, 6))]
        tools = {
            tool_name: make_tool_doc(categories)
            for tool_name in tool_names
        }
        volcano_result = VolcanoResult(tools=tools, categories=categories)
        self.generic_adder_test(volcano_result, MODULE_NAME)

    def test_run_volcano_sample_group(self):  # pylint: disable=invalid-name
        """Ensure Volcano run_sample_group produces correct results."""
        def create_sample(i):
            """Create unique sample for index i."""
            args = {
                'name': f'Sample{i}',
                'metadata': {'foobar': f'baz{i}'},
                CARDAMRResultModule.name(): create_card_amr(),
                KrakenResultModule.name(): create_kraken(),
                Metaphlan2ResultModule.name(): create_metaphlan2(),
            }
            return Sample(**args).save()

        self.generic_run_group_test(create_sample, VolcanoDisplayModule, nsamples=40)
