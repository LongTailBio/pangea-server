"""Run middleware tasks for a given sample or group."""

import networkx as nx
from celery import group as task_group

from app.analysis_modules import MODULES_BY_NAME

from .tasks import clean_error
from .utils import run_sample, run_sample_group


class TaskConductor:
    """Build chains of tasks."""

    def __init__(self, uuid, module_names=None, group=False):
        """Build a TaskConductor."""
        self.uuid = uuid
        self.group = group
        self.module_names = self._filter_module_names(module_names)
        self.signature_tbl = {}

    def _filter_module_names(self, module_names):
        """Return a list of modules that can be processed at this level."""
        if not module_names:
            module_names = list(MODULES_BY_NAME.keys())
        return [
            module_name for module_name in module_names
            if self.filter_func(module_name)
        ]

    def build_sig(self, module_name):
        """Build a signature for a single module."""
        if self.group:
            return run_sample_group.si(self.uuid, module_name).on_error(clean_error.s())
        return run_sample.s(self.uuid, module_name).on_error(clean_error.s())

    def build_depend_digraph(self):
        """Build a digraph representing module dependencies."""
        def recurse_depends(source_module, depend_graph):
            """Recursively add dependency edges to the depend graph."""
            for depends_module in source_module.required_modules():
                depend_graph.add_edge(source_module.name(), depends_module.name())
                recurse_depends(depends_module, depend_graph)

        depend_graph = nx.DiGraph()
        for module_name in self.module_names:
            recurse_depends(MODULES_BY_NAME[module_name], depend_graph)
        return depend_graph

    def recurse_chords(self, source_module_name, depend_graph):
        """Build a tree of tasks. Return the signature."""
        try:
            source_signature = self.signature_tbl[source_module_name]
        except KeyError:
            source_signature = self.build_sig(source_module_name)
            self.signature_tbl[source_module_name] = source_signature
        depends_on_chord = [
            self.recurse_chords(upstream_name, depend_graph)
            for upstream_name in nx.descendants(depend_graph, source_module_name)
            if self.filter_func(upstream_name)
        ]
        if not depends_on_chord:
            return source_signature
        return task_group(depends_on_chord) | source_signature

    def build_task_signatures(self):
        """Return a list of signatures for each origin task."""
        depend_graph = self.build_depend_digraph()
        task_signatures = [
            self.recurse_chords(module_name, depend_graph)
            for module_name in depend_graph.nodes()
            if depend_graph.in_degree(module_name) == 0
        ]
        return task_signatures

    def shake_that_baton(self):
        """Build and run task signatures."""
        signatures = self.build_task_signatures()
        for signature in signatures:
            signature.delay()
