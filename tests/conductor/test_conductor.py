"""Test suite for DisplayModuleConductors."""

from uuid import uuid4

from tool_packages.kraken import KrakenResultModule

from app.conductor import DisplayModuleConductor, SampleConductor
from app.display_modules.sample_similarity import SampleSimilarityDisplayModule
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from tests.base import BaseTestCase


KRAKEN_NAME = KrakenResultModule.name()
KRAKENHLL_NAME = KrakenHLLResultModule.name()
METAPHLAN2_NAME = Metaphlan2ResultModule.name()


class TestDisplayModuleConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    def test_downstream_modules(self):
        """Ensure downstream_modules is computed correctly."""
        downstream_modules = DisplayModuleConductor.downstream_modules(KrakenResultModule)
        self.assertIn(SampleSimilarityDisplayModule, downstream_modules)


class TestSampleConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    def test_get_valid_modules(self):
        """Ensure valid_modules is computed correctly."""
        tools_present = set([KRAKEN_NAME, KRAKENHLL_NAME, METAPHLAN2_NAME])
        downstream_modules = SampleConductor.downstream_modules(KrakenResultModule)
        sample_id = str(uuid4())
        conductor = SampleConductor(sample_id, downstream_modules)
        valid_modules = conductor.get_valid_modules(tools_present)
        self.assertIn(SampleSimilarityDisplayModule, valid_modules)

    def test_partial_valid_modules(self):
        """Ensure valid_modules is computed correctly if tools are missing."""
        tools_present = set([KRAKEN_NAME])
        downstream_modules = SampleConductor.downstream_modules(KrakenResultModule)
        sample_id = str(uuid4())
        conductor = SampleConductor(sample_id, downstream_modules)
        valid_modules = conductor.get_valid_modules(tools_present)
        self.assertTrue(SampleSimilarityDisplayModule not in valid_modules)


class TestGroupConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    pass
