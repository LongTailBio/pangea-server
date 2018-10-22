"""Test suite for TaskConductor."""

import networkx as nx
from uuid import uuid4

from analysis_packages.base_data.kraken import KrakenResultModule
from analysis_packages.base_data.krakenhll import KrakenHLLResultModule
from analysis_packages.base_data.metaphlan2 import Metaphlan2ResultModule

from app.analysis_modules.task_graph import TaskConductor
from analysis_packages.sample_similarity import SampleSimilarityAnalysisModule
from tests.base import BaseTestCase


KRAKEN_NAME = KrakenResultModule.name()
KRAKENHLL_NAME = KrakenHLLResultModule.name()
METAPHLAN2_NAME = Metaphlan2ResultModule.name()
SAMPLE_SIMILARITY_NAME = SampleSimilarityAnalysisModule.name()


class TestTaskConductor(BaseTestCase):
    """Test suite for display module Conductor."""

    def test_build_depend_digraph(self):
        """Ensure the dependency digraph is built correctly."""
        task_conductor = TaskConductor(str(uuid4()), [SAMPLE_SIMILARITY_NAME], group=True)
        depend_graph = task_conductor.build_depend_digraph()
        upstream_modules = nx.descendants(depend_graph, SAMPLE_SIMILARITY_NAME)
        self.assertIn(KRAKEN_NAME, upstream_modules)
        self.assertIn(KRAKENHLL_NAME, upstream_modules)
        self.assertIn(METAPHLAN2_NAME, upstream_modules)

    def test_build_task_signatures(self):
        """Ensure task signatures are built correctly."""
        task_conductor = TaskConductor(str(uuid4()), [SAMPLE_SIMILARITY_NAME], group=True)
        task_conductor.build_task_signatures()  # TODO: explicit checks for issues
