# pylint: disable=invalid-name

"""Modules for genomic analysis tool outputs."""

from tool_packages.base import SampleToolResultModule, GroupToolResultModule
from tool_packages.base.tests import get_result_module

from .wrangler import all_tool_results as new_results

all_tool_results = [get_result_module(module) for module in new_results]


all_group_results = [tool for tool in all_tool_results
                     if issubclass(tool, GroupToolResultModule)]


all_sample_results = [tool for tool in all_tool_results
                      if issubclass(tool, SampleToolResultModule)]
