"""Tasks for generating Top Taxa Size results."""

from pandas import DataFrame

from app.extensions import celery
from app.display_modules.utils import persist_result_helper
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule

from .constants import MODULE_NAME
from .models import TopTaxaResult

KRAKENHLL = KrakenHLLResultModule.name()
METAPHLAN = Metaphlan2ResultModule.name()


def filter_to_species_and_normalize(taxa_vec):
    """Remove everything but species and normalize."""
    out = {}
    total_count = 0
    for name, val in taxa_vec.items():
        last_taxa = name.split('|')[-1]
        if 's__' in last_taxa:
            last_taxa = ' '.join(last_taxa.split('__')[-1].split('_'))
            out[last_taxa] = val
            total_count += val
    return {name: val / total_count for name, val in taxa_vec.items()}


def taxa_in_kingdom(sample, tool_name, kingdom):
    """Return taxa in the given kingdom."""
    if kingdom == 'all_kingdoms':
        out = filter_to_species_and_normalize(sample[tool_name]['taxa'])
    else:
        raise ValueError(f'Kingdom {kingdom} not found.')
    return out


def abund_prev(taxa_vecs, top_n=50):
    """Return abundance and prevalence for topn taxa."""
    taxa_df = DataFrame(taxa_vecs).fillna(0)
    taxa_means = taxa_df.mean(axis=0)
    taxa_means = taxa_means.nlargest(top_n)

    prevalence = {}
    for taxa_name in taxa_means.index:
        one_taxa = taxa_df[taxa_name]
        taxa_prev = one_taxa[one_taxa > 0].count() / len(taxa_vecs)
        prevalence[taxa_name] = taxa_prev

    return {'abundance': taxa_means, 'prevalence': prevalence}


@celery.task()
def find_top_taxa(samples):
    """Return top taxa organized by metadata and kingdoms."""
    taxa_vecs = {}
    key_sets = []
    for sample in samples:
        for metadata_cat, metadata_val in sample['metadata'].items():
            if metadata_cat not in taxa_vecs:
                taxa_vecs[metadata_cat] = {}
            if metadata_val not in taxa_vecs[metadata_cat]:
                taxa_vecs[metadata_cat][metadata_val] = {}
            for tool in [KRAKENHLL, METAPHLAN]:
                if tool not in taxa_vecs[metadata_cat][metadata_val]:
                    taxa_vecs[metadata_cat][metadata_val][tool] = {}
                for kingdom in ['all_kingdoms']:
                    if kingdom not in taxa_vecs[metadata_cat][metadata_val][tool]:
                        taxa_vecs[metadata_cat][metadata_val][tool][kingdom] = []
                        key_sets.append((metadata_cat, metadata_val, tool, kingdom))
                    taxa_vecs[metadata_cat][metadata_val][tool][kingdom].append(
                        taxa_in_kingdom(sample, tool, kingdom)
                    )

    for metadata_cat, metadata_val, tool, kingdom in key_sets:
        my_vecs = taxa_vecs[metadata_cat][metadata_val][tool][kingdom]
        taxa_vecs[metadata_cat][metadata_val][tool][kingdom] = abund_prev(my_vecs)

    return taxa_vecs


@celery.task(name='top_taxa.persist_result')
def persist_result(result_data, analysis_result_id):
    """Persist AGS results."""
    result = TopTaxaResult(categories=result_data)
    persist_result_helper(result, analysis_result_id, MODULE_NAME)
