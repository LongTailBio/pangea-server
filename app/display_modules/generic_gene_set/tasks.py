"""Tasks for generating VFDB results."""

import numpy as np
import pandas as pd

from app.extensions import celery


def transform_sample(vfdb_tool_result, gene_names):
    """Transform sample values to rpkm output."""
    out = {'rpkm': {}, 'rpkmg': {}}
    for gene_name in gene_names:
        try:
            vals = vfdb_tool_result.genes[gene_name]
            rpkm, rpkmg = vals['rpkm'], vals['rpkmg']
        except KeyError:
            rpkm, rpkmg = 0, 0
        out['rpkm'][gene_name] = rpkm
        out['rpkmg'][gene_name] = rpkmg
    return out


@celery.task()
def filter_gene_results(samples, tool_result_name, result_type, top_n):  # pylint disable=too-many-locals
    """Reduce Methyl results to the <top_n> mean abundance genes (rpkm)."""
    sample_dict = {sample.name: getattr(sample, tool_result_name)
                   for sample in samples}
    rpkm_dict = {}
    for sname, methyl_tool_result in sample_dict.items():
        rpkm_dict[sname] = {}
        for gene, vals in methyl_tool_result.genes.items():
            rpkm_dict[sname][gene] = vals['rpkm']

    # Columns are samples, rows are genes, vals are rpkms
    rpkm_tbl = pd.DataFrame(rpkm_dict).fillna(0)
    rpkm_mean = np.array(rpkm_tbl.mean(axis=0))

    idx = (-1 * rpkm_mean).argsort()[:top_n]
    gene_names = set(rpkm_tbl.index[idx])

    filtered_sample_tbl = {sname: transform_sample(vfdb_tool_result, gene_names)
                           for sname, vfdb_tool_result in sample_dict.items()}

    result = result_type(samples=filtered_sample_tbl)
    assert result is not None
    return result
