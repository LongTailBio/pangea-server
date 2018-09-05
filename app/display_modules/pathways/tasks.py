"""Tasks for pathways module."""

import pandas as pd
import numpy as np

from tool_packages.humann2 import Humann2ResultModule

from app.extensions import celery
from app.display_modules.utils import persist_result_helper

from .constants import TOP_N
from .models import PathwayResult


def pathways_from_sample(sample):
    """Get pathways from a humann2 result."""
    module_name = Humann2ResultModule.name()
    return sample[module_name]['pathways']


def get_abund_tbl(sample_dict):
    """Return a tbl of abundances and a vector of means."""
    abund_dict = {}
    for sname, path_tbl in sample_dict.items():
        abund_dict[sname] = {}
        for path_name, vals in path_tbl.items():
            if 'unintegrated' in path_name.lower():
                continue
            abund_dict[sname][path_name] = vals['abundance']

    # Columns are samples, rows are pathways, vals are abundances
    abund_tbl = pd.DataFrame(abund_dict).fillna(0)
    abund_mean = np.array(abund_tbl.mean(axis=1))
    return abund_tbl, abund_mean


def get_top_paths(abund_tbl, abund_mean, top_n):
    """Return the names of the top_n most abundant paths.

    N.B. abund_mean is a numpy array
    """
    idx = (-1 * abund_mean).argsort()[:top_n]
    path_names = set(abund_tbl.index[idx])
    return path_names


@celery.task()
def filter_humann2_pathways(samples):
    """Get the top N mean abundance pathways."""
    sample_dict = {sample['name']: pathways_from_sample(sample)
                   for sample in samples}

    abund_tbl, abund_mean = get_abund_tbl(sample_dict)
    path_names = get_top_paths(abund_tbl, abund_mean, TOP_N)

    out = {}
    for sname, path_tbl in sample_dict.items():
        path_abunds = {}
        path_covs = {}
        for path_name in path_names:
            try:
                abund = path_tbl[path_name]['abundance']
                cov = path_tbl[path_name]['coverage']
            except KeyError:
                abund = 0
                cov = 0
            path_abunds[path_name] = np.log10(abund + 1)
            path_covs[path_name] = cov

        out[sname] = {'pathway_abundances': path_abunds,
                      'pathway_coverages': path_covs}

    result_data = {'samples': out}
    return result_data


@celery.task(name='pathways.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Pathways results."""
    result = PathwayResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
