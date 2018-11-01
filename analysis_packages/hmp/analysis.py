"""Tasks to process HMP results."""

from numpy import percentile

from analysis_packages.base.utils import categories_from_metadata, scrub_category_val
from tool_packages.hmp_sites import HmpSitesResultModule


def make_dist_table(hmp_results, site_names):
    """Make a table of distributions, one distribution per site."""
    sites = []
    for site_name in site_names:
        sites.append([])
        for hmp_result in hmp_results:
            for measure in hmp_result[site_name]:
                if measure > 0:
                    sites[-1].append(measure)

    def get_percentile(measurements):
        """Get percentiles or return null values."""
        if measurements:
            return percentile(measurements, [0, 25, 50, 75, 100]).tolist()
        return [0] * 5

    dists = [get_percentile(measurements)
             for measurements in sites]
    return dists


def make_distributions(categories, samples):
    """Determine HMP distributions by site and category."""
    tool_name = HmpSitesResultModule.name()
    site_names = HmpSitesResultModule.result_model().site_names()

    distributions = {}
    for category_name, category_values in categories.items():
        table = {category_value: [] for category_value in category_values}
        for sample in samples:
            hmp_result = sample[tool_name]
            sample_cat_val = sample['metadata'][category_name]
            sample_cat_val = scrub_category_val(sample_cat_val)
            table[sample_cat_val].append(hmp_result)
        distributions[category_name] = [
            {'name': scrub_category_val(category_value),
             'data': make_dist_table(hmp_results, site_names)}
            for category_value, hmp_results in table.items()]

    result_data = {
        'categories': categories,
        'sites': site_names,
        'data': distributions,
    }
    return result_data


def processor(*samples):
    """Handle HMP component calculations."""
    categories = categories_from_metadata(samples)
    distributions = make_distributions(categories, samples)
    return distributions
