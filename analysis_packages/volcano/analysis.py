"""Tasks to process Volcano results."""

import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu

from analysis_packages.base.utils import categories_from_metadata
from tool_packages.kraken import KrakenResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule


MIN_VEC_LEN = 4


def clean_vector(vec):
    """Clean a taxa vec."""
    out = {}
    for key, val in vec.items():
        new_key = key.split('|')[-1]
        new_key = new_key.split('__')[-1]
        out[new_key] = val
    return out


def make_dataframe(samples, tool_name, dataframe_key):
    """Return a pandas dataframe for the given tool."""
    tbl = {}
    for sample in samples:
        tbl[sample['name']] = clean_vector(sample[tool_name][dataframe_key])
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
        col_cases_array = col_cases.values
        col_controls_array = col_controls.values
        try:
            _, pval = mannwhitneyu(col_cases_array, col_controls_array, alternative=None)
        except ValueError:
            return 0
        pval *= 2  # correct for two sided
        assert 0.0 < pval <= 1.0, f'cases: {col_cases}\ncontrols: {col_controls}'
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
            if bin_start <= pval < bin_end:
                bins[bin_start] += 1
                break
    pts = [{'name': f'histo_{bin_start}', 'xval': bin_start, 'yval': nps}
           for bin_start, nps in bins.items()]
    return pts


def filter_nans(points):
    """Remove points that have nans or infinites."""
    def test_point(point):
        """Test a single point for validity."""
        for coord in ['xval', 'yval', 'zval']:
            value = point[coord]
            # isfinite checks against infinity and nan
            if not np.isfinite(value):
                return False
        return True

    result = [point for point in points if test_point(point)]
    return result


def handle_one_tool_category(category_name, category_value,
                             samples, tool_name, dataframe_key):
    """Return the JSON for a ToolCategoryDocument."""
    cases, controls = get_cases(category_name, category_value, samples)
    if (len(cases) < MIN_VEC_LEN) or (len(controls) < MIN_VEC_LEN):
        return None

    tool_df = make_dataframe(samples, tool_name, dataframe_key)
    lfcs, case_means = get_lfcs(tool_df, cases, controls)
    nlps, pvals = get_nlps(tool_df, cases, controls)

    scatter_values = {
        'xval': lfcs,
        'yval': nlps,
        'zval': case_means,
        'name': list(tool_df.columns.values),
    }
    scatter_plot = pd.DataFrame(scatter_values).to_dict(orient='records')
    scatter_plot = filter_nans(scatter_plot)
    if not scatter_plot:
        return None

    out = {
        'scatter_plot': scatter_plot,
        'pval_histogram': pval_hist(pvals),
    }
    return out


def store_scatter_plot(out, tool_name, cat_name, cat_value, scatter_plot):
    """Store a scatter plot to out, if appropriate."""
    if scatter_plot is None:
        return
    try:
        tool_tbl = out['tools'][tool_name]['tool_categories']
    except KeyError:
        out['tools'][tool_name] = {'tool_categories': {}}
        tool_tbl = out['tools'][tool_name]['tool_categories']

    try:
        out['categories'][cat_name].append(cat_value)
    except KeyError:
        out['categories'][cat_name] = [cat_value]
    try:
        tool_tbl[cat_name][cat_value] = scatter_plot
    except KeyError:
        tool_tbl[cat_name] = {cat_value: scatter_plot}


def make_volcanos(categories, samples):
    """Return the JSON for a VolcanoResult."""
    dataframe_keys = {
        KrakenResultModule.name(): 'taxa',
        Metaphlan2ResultModule.name(): 'taxa',
    }
    out = {'categories': {}, 'tools': {}}
    for tool_name, dataframe_key in dataframe_keys.items():
        for category_name, category_values in categories.items():
            for category_value in category_values:
                scatter_plot = handle_one_tool_category(
                    category_name,
                    category_value,
                    samples,
                    tool_name,
                    dataframe_key,
                )
                store_scatter_plot(out, tool_name, category_name, category_value, scatter_plot)
    return out


def processor(*samples):
    """Handle Volcano component calculations."""
    categories = categories_from_metadata(samples, min_size=1)
    return make_volcanos(categories, samples)
