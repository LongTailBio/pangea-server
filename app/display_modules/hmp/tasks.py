"""Tasks to process HMP results."""

from numpy import percentile

from app.extensions import celery
from app.display_modules.utils import persist_result_helper
from app.tool_results.hmp_sites import HmpSitesResultModule

from .models import HMPResult


def make_dist_table(hmp_results, site_names):
    """Make a table of distributions, one distribution per site."""
    sites = []
    for site_name in site_names:
        sites.append([])
        for hmp_result in hmp_results:
            sites[-1] += hmp_result[site_name]
    dists = [percentile(measurements, [0, 25, 50, 75, 100]).tolist()
             for measurements in sites]
    return dists


@celery.task()
def make_distributions(categories, samples):
    """Determine HMP distributions by site and category."""
    tool_name = HmpSitesResultModule.name()
    site_names = HmpSitesResultModule.result_model().site_names()

    distributions = {}
    for category_name, category_values in categories.items():
        table = {category_value: [] for category_value in category_values}
        for sample in samples:
            hmp_result = sample[tool_name]
            table[sample['metadata'][category_name]].append(hmp_result)
        distributions[category_name] = [
            {'name': category_value,
             'data': make_dist_table(hmp_results, site_names)}
            for category_value, hmp_results in table.items()]

    result_data = {
        'categories': categories,
        'sites': site_names,
        'data': distributions,
    }
    return result_data


@celery.task(name='hmp.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist HMP results."""
    result = HMPResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
