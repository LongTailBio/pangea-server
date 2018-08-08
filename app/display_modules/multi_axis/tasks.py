"""Tasks for generating Sample Similarity results."""

from pandas import DataFrame
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale as center_and_scale

from app.extensions import celery
from app.display_modules.utils import persist_result_helper, scrub_category_val
from app.tool_results.card_amrs import CARDAMRResultModule
from app.tool_results.humann2_normalize import Humann2NormalizeResultModule
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.microbe_census import MicrobeCensusResultModule

from .constants import MODULE_NAME
from .models import MultiAxisResult


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
    return data_matrix.mean(axis=0)


def make_taxa_axes(samples, axes):
    """Build taxa axes for the samples."""
    for module in [KrakenHLLResultModule, Metaphlan2ResultModule]:
        taxa_matrix = module.promote_vectors(samples, normalize_rows=True)['taxa']
        taxa_pca = run_pca(taxa_matrix)
        for col_name, axis in taxa_pca.items():
            axis_name = module.name() + f'_{col_name}'
            axes[axis_name] = axis.to_dict()


def make_gene_axes(samples, axes):
    """Build gene axes for the samples."""
    for module in [Humann2NormalizeResultModule, CARDAMRResultModule]:
        gene_matrix = module.promote_vectors(samples, extractor=lambda x: x['rpkm'])['genes']
        axis_name = module.name() + f'_mean'
        axes[axis_name] = sample_mean(gene_matrix).to_dict()
        gene_pca = run_pca(gene_matrix)
        for col_name, axis in gene_pca.items():
            axis_name = module.name() + f'_{col_name}'
            axes[axis_name] = axis.to_dict()


@celery.task()
def make_axes(samples):
    """Return a dict of axes with names."""
    ags = 'average_genome_size'
    axes = {
        ags: MicrobeCensusResultModule.promote_scalars(samples)[ags].to_dict()
    }
    make_taxa_axes(samples, axes)
    make_gene_axes(samples, axes)
    return {axis_name: {'vals': axis_vals} for axis_name, axis_vals in axes.items()}


@celery.task()
def multi_axis_reducer(args, samples):
    """Combine multi axis components."""
    axes = args[0]
    categories = args[1]
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
    print(result_data)
    return result_data


@celery.task(name='multi_axis.persist_result')
def persist_result(result_data, analysis_result_id):
    """Persist Microbe Directory results."""
    result = MultiAxisResult(**result_data)
    persist_result_helper(result, analysis_result_id, MODULE_NAME)
