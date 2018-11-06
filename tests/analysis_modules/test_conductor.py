"""Test suite for TaskConductor."""

from uuid import uuid4
import networkx as nx

from analysis_packages.krakenhll_data import KrakenHLLResultModule
from analysis_packages.metaphlan2_data import Metaphlan2ResultModule
from analysis_packages.sample_similarity import SampleSimilarityAnalysisModule

from app.analysis_modules.task_graph import TaskConductor
from tests.base import BaseTestCase


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
        self.assertIn(KRAKENHLL_NAME, upstream_modules)
        self.assertIn(METAPHLAN2_NAME, upstream_modules)

    def test_build_task_signatures(self):
        """Ensure task signatures are built correctly."""
        task_conductor = TaskConductor(str(uuid4()), [SAMPLE_SIMILARITY_NAME], group=True)
        task_sigs = task_conductor.build_task_signatures()
        self.assertTrue(len(task_sigs) == 3)
