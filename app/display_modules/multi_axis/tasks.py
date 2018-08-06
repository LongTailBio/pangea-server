"""Tasks for generating Sample Similarity results."""

from sklearn.decomposition import PCA
from sklearn.preprocessing import scale as center_and_scale

from app.extensions import celery
from app.display_modules.utils import persist_result_helper
from app.tool_results.card_amrs import CARDAMRResultModule
from app.tool_results.humann2_normalize import Humann2NormalizeResultModule
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule
from app.tool_results.microbe_census import MicrobeCensusResultModule

from .models import MultiAxisResult


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


def make_taxa_axes(samples, axes):
    """Build taxa axes for the samples."""

    for module in [KrakenHLLResultModule, Metaphlan2ResultModule]:
        taxa_matrix = module.promote_vectors(samples, normalize_rows=True)['taxa']
        taxa_pca = run_pca(taxa_matrix)
        for i, axis in enumerate(taxa_pca):
            axis_name = module.name() + f'_PC_{i}'
            axes[axis_name] = axis


def make_gene_axes(samples, axes):
    """Build gene axes for the samples."""

    for module in [Humann2NormalizeResultModule, CARDAMRResultModule]:
        gene_matrix = module.promote_vectors(samples, extractor=lambda x: x['rpkm'])['genes']
        axis_name = module.name() + f'_mean'
        axes[axis_name] = sample_mean(gene_matrix)
        gene_pca = run_pca(gene_matrix)
        for i, axis in enumerate(gene_pca):
            axis_name = module.name() + f'_PC_{i}'
            axes[axis_name] = axis


@celery.task(name='multi_axis.make_axes')
def make_axes(samples):
    """Return a dict of axes with names."""
    ags = 'average_genome_size'
    axes = {
        ags: MicrobeCensusResultModule.promote_scalars(samples)[ags]
    }
    make_taxa_axes(samples, axes)
    make_gene_axes(samples, axes)
    return axes


@celery.task(name='multi_axis.persist_result')
def persist_result(axes, categories, analysis_result_id, result_name):
    """Persist Microbe Directory results."""
    result_data = {
        'axes': axes,
        'categories': categories,
    }
    result = MultiAxisResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
