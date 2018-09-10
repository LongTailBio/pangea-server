"""Test suite for DisplayModuleConductors."""

from uuid import uuid4

from tool_packages.kraken import KrakenResultModule
from tool_packages.krakenhll import KrakenHLLResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule

from app.analysis_modules.conductor import DisplayModuleConductor, SampleConductor
from analysis_packages.sample_similarity import SampleSimilarityAnalysisModule
from tests.base import BaseTestCase


KRAKEN_NAME = KrakenResultModule.name()
KRAKENHLL_NAME = KrakenHLLResultModule.name()
METAPHLAN2_NAME = Metaphlan2ResultModule.name()


class TestDisplayModuleConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    def test_downstream_modules(self):
        """Ensure downstream_modules is computed correctly."""
        downstream_modules = DisplayModuleConductor.downstream_modules(KrakenResultModule)
        self.assertIn(SampleSimilarityAnalysisModule, downstream_modules)


class TestSampleConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    def test_get_valid_modules(self):
        """Ensure valid_modules is computed correctly."""
        tools_present = set([KRAKEN_NAME, KRAKENHLL_NAME, METAPHLAN2_NAME])
        downstream_modules = SampleConductor.downstream_modules(KrakenResultModule)
        sample_id = str(uuid4())
        conductor = SampleConductor(sample_id, downstream_modules)
        valid_modules = conductor.get_valid_modules(tools_present)
        self.assertIn(SampleSimilarityAnalysisModule, valid_modules)

    def test_partial_valid_modules(self):
        """Ensure valid_modules is computed correctly if tools are missing."""
        tools_present = set([KRAKEN_NAME])
        downstream_modules = SampleConductor.downstream_modules(KrakenResultModule)
        sample_id = str(uuid4())
        conductor = SampleConductor(sample_id, downstream_modules)
        valid_modules = conductor.get_valid_modules(tools_present)
        self.assertTrue(SampleSimilarityAnalysisModule not in valid_modules)


class TestGroupConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    pass
