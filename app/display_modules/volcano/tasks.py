"""Tasks to process Volcano results."""

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from app.display_modules.utils import persist_result_helper
from app.extensions import celery
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule

from .models import VolcanoResult


def clean_vector(vec):
    """Clean a taxa vec."""
    out = {}
    for key, val in vec.items():
        new_key = key.split('|')[-1]
        new_key = new_key.split('__')[-1]
        out[new_key] = val
    return out


def make_dataframe(samples, tool_name):
    """Return a pandas dataframe for the given tool."""
    key = 'taxa'  # this will eventually change based on tool name
    tbl = {}
    for sample in samples:
        tbl[sample['name']] = clean_vector(sample[tool_name][key])
    tool_tbl = pd.DataFrame.from_dict(tbl, orient='index', dtype=np.float64)  # pylint: disable=no-member
    return tool_tbl.fillna(0)


def get_cases(category_name, category_value, samples):
    """Return sets for case and control sample names."""
    cases, controls = set(), set()
    for sample in samples:
        if sample['metadata'][category_name] == category_value:
            cases.add(sample['name'])
            continue
        controls.add(sample['name'])
    return cases, controls


def get_lfcs(tool_df, cases, controls):
    """Return two series: LFC of means and mean of cases."""
    case_means = tool_df.loc[cases].mean(axis=0)
    control_means = tool_df.loc[controls].mean(axis=0)
    lfcs = (case_means / control_means).apply(np.log2)
    return lfcs, case_means


def get_nlps(tool_df, cases, controls):
    """Return a series of nlps for each column and a list of raw pvalues."""
    pvals = []

    def mwu(col_cases, col_controls):
        """Perform MWU test on a column of the dataframe."""
        col_cases_array = col_cases.as_matrix()
        col_controls_array = col_controls.as_matrix()
        _, pval = mannwhitneyu(col_cases_array, col_controls_array)

        pval *= 2  # correct for two sided
        assert pval <= 1.0
        pvals.append(pval)
        nlp = -np.log10(pval)
        return nlp

    nlps = {}
    for col_name in tool_df:
        col = tool_df[col_name]
        col_cases = col[cases]
        col_controls = col[controls]
        nlps[col_name] = mwu(col_cases, col_controls)
    nlps = pd.Series(nlps)

    return nlps, pvals


def pval_hist(pvals, bin_width=0.05):
    """Return a histogram of pvalues."""
    nbins = int(1 / bin_width + 0.5)
    bins = {bin_width * i: 0
            for i in range(nbins)}
    for pval in pvals:
        for bin_start in bins:
            bin_end = bin_start + bin_width
            if (pval >= bin_start) and (pval < bin_end):
                bins[bin_start] += 1
                break

    pts = [{'xval': bin_start, 'yval': nps}
           for bin_start, nps in bins.items()]
    return pts


def handle_one_tool_category(category_name, category_value, samples, tool_name):
    """Return the JSON for a ToolCategoryDocument."""
    tool_df = make_dataframe(samples, tool_name)
    cases, controls = get_cases(category_name, category_value, samples)
    lfcs, case_means = get_lfcs(tool_df, cases, controls)
    nlps, pvals = get_nlps(tool_df, cases, controls)

    out = {
        'scatter_plot': pd.DataFrame({
            'xval': lfcs,
            'yval': nlps,
            'zval': case_means,
            'name': tool_df.index.to_series(),
        }).to_dict(orient='records'),
        'pval_histogram': pval_hist(pvals)
    }
    return out


@celery.task()
def make_volcanos(categories, samples):
    """Return the JSON for a VolcanoResult."""
    tool_names = [
        KrakenResultModule.name(),
        Metaphlan2ResultModule.name(),
    ]
    out = {'categories': categories, 'tools': {}}
    for tool_name in tool_names:
        out['tools'][tool_name] = {'tool_categories': {}}
        tool_tbl = out['tools'][tool_name]['tool_categories']
        for category_name, category_values in categories.items():
            tool_tbl[category_name] = {}
            for category_value in category_values:
                tool_tbl[category_name][category_value] = handle_one_tool_category(
                    category_name,
                    category_value,
                    samples,
                    tool_name,
                )
    return out


@celery.task(name='volcano.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Microbe Directory results."""
    result = VolcanoResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
