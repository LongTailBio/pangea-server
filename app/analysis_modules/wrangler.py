"""Gather all installed AnalysisModule packages."""

import pkgutil

import analysis_packages
from analysis_packages.base.utils import get_primary_module


def discover_local_packages():
    """Construct list of local AnalysisModule packages."""
    package = analysis_packages
    path = package.__path__
    prefix = f'{package.__name__}.'

    results = []
    for _, modname, _ in pkgutil.iter_modules(path, prefix):
        blacklist = [
            'analysis_packages', 'analysis_packages.base', 'analysis_packages.generic_gene_set'
        ]
        if modname not in blacklist:
            # Pass dummy value to fromlist in order to import all module members
            module = __import__(modname, fromlist='dummy')
            results.append(module)

    return results


# pylint:disable=invalid-name

all_analysis_packages = discover_local_packages()


all_analysis_modules = [get_primary_module(package) for package in all_analysis_packages]


MODULES_BY_NAME = {module.name(): module for module in all_analysis_modules}
