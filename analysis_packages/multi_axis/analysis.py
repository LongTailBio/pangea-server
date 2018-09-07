"""Tasks for generating Sample Similarity results."""

from pandas import DataFrame
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale as center_and_scale

from analysis_packages.base.utils import scrub_category_val, categories_from_metadata
from analysis_packages.base.exceptions import UnsupportedAnalysisMode
from tool_packages.card_amrs import CARDAMRResultModule
from tool_packages.humann2_normalize import Humann2NormalizeResultModule
from tool_packages.krakenhll import KrakenHLLResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule
from tool_packages.microbe_census import MicrobeCensusResultModule


def run_pca(data_matrix, n_components=3):
    """Run PCA on a matrix returning the <N> largest components.

    data_matrix is standard form, observations in the rows and
    dimensions in columns.
    """
    data_matrix = data_matrix.fillna(0)
    scaled_data_matrix = center_and_scale(data_matrix)
    pca = PCA(n_components=n_components, whiten=True)
    pca_matrix = pca.fit_transform(scaled_data_matrix)
    return DataFrame(
        pca_matrix,
        columns=[f'PC_{i}' for i in range(n_components)],
        index=data_matrix.index
    )


def sample_mean(data_matrix):
    """Return a vector giving the average value for all observations."""
    data_matrix = data_matrix.fillna(0)
    return data_matrix.mean(axis=1)  # row-wise mean


def fill_taxa_axes(samples, axes):
    """Build taxa axes for the samples."""
    for module in [KrakenHLLResultModule, Metaphlan2ResultModule]:
        taxa_matrix = module.promote_vectors(samples, normalize_rows=True)['taxa']
        taxa_pca = run_pca(taxa_matrix)
        for col_name, axis in taxa_pca.items():
            axis_name = f'{module.name()}_{col_name}'
            axes[axis_name] = axis.to_dict()


def fill_gene_axes(samples, axes):
    """Build gene axes for the samples."""
    for module in [Humann2NormalizeResultModule, CARDAMRResultModule]:
        gene_matrix = module.promote_vectors(samples, extractor=lambda x: x['rpkm'])['genes']
        axis_name = f'{module.name()}_mean'
        axes[axis_name] = sample_mean(gene_matrix).to_dict()
        gene_pca = run_pca(gene_matrix)
        for col_name, axis in gene_pca.items():
            axis_name = f'{module.name()}_{col_name}'
            axes[axis_name] = axis.to_dict()


def make_axes(samples):
    """Return a dict of axes with names."""
    ags = 'average_genome_size'
    axes = {
        ags: MicrobeCensusResultModule.promote_scalars(samples)[ags].to_dict()
    }
    fill_taxa_axes(samples, axes)
    fill_gene_axes(samples, axes)
    return {axis_name: {'vals': axis_vals} for axis_name, axis_vals in axes.items()}


def multi_axis_reducer(axes, categories, samples):
    """Combine multi axis components."""
    metadata = {}
    for sample in samples:
        metadata[sample['name']] = {}
        for category_name in categories.keys():
            category_value = sample['metadata'].get(category_name, 'None')
            category_value = scrub_category_val(category_value)
            metadata[sample['name']][category_name] = category_value

    result_data = {
        'axes': axes,
        'categories': categories,
        'metadata': metadata,
    }
    return result_data


def processor(*samples):
    """Handle Multi-Axis component calculations."""
    samples = list(samples)
    if len(samples) <= 1:
        raise UnsupportedAnalysisMode

    axes = make_axes(samples)
    categories = categories_from_metadata(samples)
    return multi_axis_reducer(axes, categories, samples)
