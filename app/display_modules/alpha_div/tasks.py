"""Tasks to process Alpha Diversity results."""

from numpy import percentile

from tool_packages.kraken import KrakenResultModule

from app.extensions import celery
from app.display_modules.utils import persist_result_helper, scrub_category_val
from app.tool_results.alpha_diversity import AlphaDiversityToolResult
from app.tool_results.metaphlan2 import Metaphlan2ResultModule

from .models import AlphaDiversityResult

# Define aliases
ADivRes = AlphaDiversityToolResult  # pylint: disable=invalid-name


def tool_name_to_param(tool_name):
    """Convert tool short names to param names."""
    for param_name in [KrakenResultModule.name(), Metaphlan2ResultModule.name()]:
        if tool_name in param_name:
            return param_name
    return tool_name


def make_dist(measurements):
    """Make a table of distributions, one distribution per site."""
    return percentile(measurements, [0, 25, 50, 75, 100]).tolist()


def handle_distribution_subtable(tbl, samples,                    # pylint: disable=too-many-arguments,too-many-locals
                                 tool_name, taxa_rank, cat_name,
                                 cat_vals, primary_metrics, second_metric):
    """Update table for distribution data."""
    upper_tbl = tbl[tool_name][taxa_rank][cat_name]

    for sample in samples:
        cat_val = sample['metadata'][cat_name]
        cat_val = scrub_category_val(cat_val)
        metric_tbl = upper_tbl[cat_val]
        value_tbl = sample['alpha_diversity_stats'][tool_name][taxa_rank]

        for primary_metric in primary_metrics:
            primary_table = value_tbl[primary_metric]
            try:
                val = primary_table[second_metric]
            except KeyError:  # occurs when there is only one value
                val = [val for val in primary_table.values()][0]
            metric_tbl[primary_metric].append(val)

    for primary_metric in primary_metrics:
        for cat_val in cat_vals:
            metric_vals = upper_tbl[cat_val][primary_metric]
            metric_dist = make_dist(metric_vals)
            upper_tbl[cat_val][primary_metric] = metric_dist

    flattened_vals = []
    for cat_val, metric_tbl in upper_tbl.items():
        flattened_vals.append({
            'metrics': list(primary_metrics),
            'category_value': cat_val,
            'by_metric': metric_tbl,
        })
    tbl[tool_name][taxa_rank][cat_name] = flattened_vals


@celery.task()
def make_alpha_distributions(categories, samples):
    """Determine HMP distributions by site and category."""
    tbl = {}
    for tool_name, metrics in ADivRes.metrics().items():
        tbl[tool_name] = {}
        primary_metrics, secondary_metric = metrics
        for taxa_rank in ADivRes.taxa_ranks():
            tbl[tool_name][taxa_rank] = {}
            for cat_name, cat_vals in categories.items():
                tbl[tool_name][taxa_rank][cat_name] = {
                    cat_val: {
                        primary_metric: []
                        for primary_metric in primary_metrics
                    }
                    for cat_val in cat_vals
                }
                handle_distribution_subtable(
                    tbl, samples,
                    tool_name, taxa_rank, cat_name,
                    cat_vals, primary_metrics, secondary_metric
                )
            tbl[tool_name][taxa_rank] = {
                'by_category_name': tbl[tool_name][taxa_rank],
            }
        tbl[tool_name] = {
            'taxa_ranks': [el for el in ADivRes.taxa_ranks()],
            'by_taxa_rank': tbl[tool_name],
        }
    tbl = {
        'by_tool': tbl,
        'categories': categories,
        'tool_names': [el for el in ADivRes.tool_names()],
    }
    return tbl


@celery.task(name='alpha_diversity.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Alpha Diversity results."""
    result = AlphaDiversityResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
