"""Tasks for generating Generic Gene Set results."""

import numpy as np
import pandas as pd


def transform_sample(vfdb_tool_result, gene_names):
    """Transform sample values to rpkm output."""
    out = {'rpkm': {}, 'rpkmg': {}}
    for gene_name in gene_names:
        try:
            vals = vfdb_tool_result['genes'][gene_name]
            rpkm, rpkmg = vals['rpkm'], vals['rpkmg']
        except KeyError:
            rpkm, rpkmg = 0, 0
        out['rpkm'][gene_name] = np.log10(rpkm + 1)
        out['rpkmg'][gene_name] = np.log10(rpkmg + 1)
    return out


def get_rpkm_tbl(sample_dict):
    """Return a tbl of rpkm vals and a vector of means."""
    rpkm_dict = {}
    for sname, methyl_tool_result in sample_dict.items():
        rpkm_dict[sname] = {}
        for gene, vals in methyl_tool_result['genes'].items():
            rpkm_dict[sname][gene] = vals['rpkm']

    # Columns are samples, rows are genes, vals are rpkms
    rpkm_tbl = pd.DataFrame(rpkm_dict).fillna(0)
    rpkm_mean = np.array(rpkm_tbl.mean(axis=1))
    return rpkm_tbl, rpkm_mean


def get_top_genes(rpkm_tbl, rpkm_mean, top_n):
    """Return the names of the top_n most abundant genes.

    N.B. rpkm_mean is a numpy array
    """
    idx = (-1 * rpkm_mean).argsort()[:top_n]
    gene_names = set(rpkm_tbl.index[idx])
    return gene_names


def filter_gene_results(samples, source_tool_name, top_n):
    """Reduce Methyl results to the <top_n> mean abundance genes (rpkm)."""
    sample_dict = {sample['name']: sample[source_tool_name]
                   for sample in samples}

    rpkm_tbl, rpkm_mean = get_rpkm_tbl(sample_dict)
    gene_names = get_top_genes(rpkm_tbl, rpkm_mean, top_n)

    filtered_sample_tbl = {sname: transform_sample(vfdb_tool_result, gene_names)
                           for sname, vfdb_tool_result in sample_dict.items()}

    result_data = {'samples': filtered_sample_tbl}
    return result_data
