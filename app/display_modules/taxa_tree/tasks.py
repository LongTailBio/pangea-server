"""Tasks for TaxaTree Wrangler."""

from tool_packages.kraken import KrakenResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule
from tool_packages.krakenhll import KrakenHLLResultModule

from app.extensions import celery
from app.display_modules.utils import persist_result_helper

from .models import TaxaTreeResult


def get_total(taxa_list, delim):
    """Return the total abundance in the taxa list.

    This is not the sum b/c taxa lists are trees, implicitly.
    """
    total = 0
    for taxon, abund in taxa_list.items():
        tkns = taxon.split(delim)
        if len(tkns) == 1:
            total += abund
    return total


def convert_children_to_list(taxa_tree):
    """Convert a dictionary of children to a list, recursively."""
    children = taxa_tree['children']
    taxa_tree['children'] = [convert_children_to_list(child)
                             for child in children.values()]
    return taxa_tree


def get_taxa_tokens(taxon, delim, tkn_delim='__'):
    """Return a list of cleaned tokens."""
    tkns = taxon.split(delim)
    tkns = [tkn.split(tkn_delim)[-1] for tkn in tkns]
    return tkns


def recurse_tree(tree, tkns, i, leaf_size):
    """Return a recursively built tree."""
    is_leaf = (i + 1) == len(tkns)
    tkn = tkns[i]

    try:
        tree['children'][tkn]
    except KeyError:
        tree['children'][tkn] = {
            'name': tkn,
            'parent': 'root',
            'size': -1,
            'children': {},
        }
        if i > 0:
            tree['children'][tkn]['parent'] = tkns[i - 1]
        if is_leaf:
            tree['children'][tkn]['size'] = leaf_size
    if is_leaf:
        return tree['children'][tkn]
    return recurse_tree(tree['children'][tkn], tkns, i + 1, leaf_size)


def reduce_taxa_list(taxa_list, delim='|'):
    """Return a tree built from a taxa list."""
    factor = 100 / get_total(taxa_list, delim)
    taxa_tree = {
        'name': 'root',
        'parent': None,
        'size': 100,
        'children': {}
    }
    for taxon, abund in taxa_list.items():
        tkns = get_taxa_tokens(taxon, delim)
        recurse_tree(taxa_tree, tkns, 0, factor * abund)
    taxa_tree = convert_children_to_list(taxa_tree)
    return taxa_tree


@celery.task()
def trees_from_sample(sample):
    """Build taxa trees for a given sample."""
    metaphlan2 = sample[Metaphlan2ResultModule.name()]
    metaphlan2 = reduce_taxa_list(metaphlan2['taxa'])
    kraken = sample[KrakenResultModule.name()]
    kraken = reduce_taxa_list(kraken['taxa'])
    krakenhll = sample[KrakenHLLResultModule.name()]
    krakenhll = reduce_taxa_list(krakenhll['taxa'])
    return {
        'kraken': kraken,
        'metaphlan2': metaphlan2,
        'krakenhll': krakenhll,
    }


@celery.task(name='taxa_tree.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Taxa Tree results."""
    result = TaxaTreeResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
