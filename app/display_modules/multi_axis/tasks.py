"""Tasks for generating Sample Similarity results."""

import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale as center_and_scale

from app.extensions import celery
from app.display_modules.utils import persist_result_helper, scrub_category_val
from app.tool_results.card_amrs import CARDAMRResultModule
from app.tool_results.humann2_normalize import Humann2NormalizeResultModule
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.microbe_census import MicrobeCensusResultModule

from .models import SampleSimilarityResult
from .constants import MODULE_NAME


def run_pca(data_matrix, n_components=3):
    """Run PCA on a matrix returning the <N> largest components.

    data_matrix is standard form, observations in the rows and
    dimensions in columns.
    """
    scaled_data_matrix = center_and_scale(data_matrix)
    pca = PCA(n_components=n_components, whiten=True)
    return pca.fit_transform(scaled_data_matrix)


def sample_mean(data_matrix):
    """Return a vector giving the average value for all observations."""
    return np.array(data_matrix.mean(axis=0))


def get_data_matrix(samples, tool_result_module, key, extractor=lambda x: x, normalize_rows=False):
    """Return a tbl of values"""
    tool_result_name = tool_result_module.name()
    data_tbl = {
        sample['name']: {
            feature: extractor(val)
            for feature, val in sample[tool_result_name][key].items()
        }
        for sample in samples

    }
    # Columns are samples, rows are genes, vals are rpkms
    data_tbl = pd.DataFrame.from_dict(data_tbl, orient='index').fillna(0)
    if normalize_rows:
        data_tbl = data_tbl.div(data_tbl.sum(axis=1), axis=0)
    return data_tbl


def make_taxa_axes(samples, axes):
    """Build taxa axes for the samples."""

    for module in [KrakenHLLResultModule, Metaphlan2ResultModule]:
        taxa_matrix = get_data_matrix(samples, module, 'taxa', normalize_rows=True)
        taxa_pca = run_pca(taxa_matrix)
        for i, axis in enumerate(taxa_pca):
            axis_name = module.name() + f'_PCA_{i}'
            axes[axis_name] = axis


def make_gene_axes(samples, axes):
    """Build gene axes for the samples."""

    for module in [Humann2NormalizeResultModule, CARDAMRResultModule]:
        gene_matrix = get_data_matrix(samples, module, 'genes', extractor=lambda x: x[key])
        axis_name = module.name() + f'_mean'
        axes[axis_name] = sample_mean(gene_matrix)
        gene_pca = run_pca(gene_matrix)
        for i, axis in enumerate(gene_pca):
            axis_name = module.name() + f'_PCA_{i}'
            axes[axis_name] = axis


def make_axes(samples):

    axes = {}
    make_taxa_axes(samples, axes)
    make_gene_axes(samples, axes)

    axes['average_genome_size'] = {
        sample['name']: sample[MicrobeCensusResultModule.name()]['average_genome_size']
    }
