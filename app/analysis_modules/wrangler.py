"""Gather all installed AnalysisModule packages."""

import importlib
import pkgutil

import pangea_modules
from pangea_modules.base.utils import get_primary_module


# From: https://packaging.python.org/guides/creating-and-discovering-plugins/
def iter_namespace(ns_pkg):
    """Return iterator of packages within a namespace."""
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + '.')


BLACKLIST = [
    'pangea_modules',
    'pangea_modules.base',
    'pangea_modules.generic_gene_set',
]


PANGEA_PACKAGES = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in iter_namespace(pangea_modules)
    if name not in BLACKLIST
}


MODULES_BY_NAME = {
    module.name(): module
    for module in [get_primary_module(package)
                   for package in PANGEA_PACKAGES.values()]
}


# pylint:disable=invalid-name
all_analysis_modules = list(MODULES_BY_NAME.values())
