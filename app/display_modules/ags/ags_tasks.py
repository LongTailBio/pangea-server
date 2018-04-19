"""Tasks for generating Average Genome Size results."""

from numpy import percentile

from app.extensions import celery
from app.display_modules.utils import persist_result_helper
from app.tool_results.microbe_census import MicrobeCensusResultModule

from .ags_models import AGSResult


def boxplot(values):
    """Calculate percentiles needed for a boxplot."""
    percentiles = percentile(values, [0, 25, 50, 75, 100])
    result = {'min_val': percentiles[0],
              'q1_val': percentiles[1],
              'mean_val': percentiles[2],
              'q3_val': percentiles[3],
              'max_val': percentiles[4]}
    return result


@celery.task()
def ags_distributions(samples):
    """Determine Average Genome Size distributions."""
    microbe_census_key = MicrobeCensusResultModule.name()
    ags_vals = {}
    for sample in samples:
        sample_ags = sample[microbe_census_key]['average_genome_size']
        for key, value in sample['metadata'].items():
            try:
                ags_vals[key][value].append(sample_ags)
            except KeyError:
                try:
                    ags_vals[key][value] = [sample_ags]
                except KeyError:
                    ags_vals[key] = {value: [sample_ags]}

    for category, val_dict in ags_vals.items():
        for val, ags_values in val_dict.items():
            ags_vals[category][val] = boxplot(ags_values)

    return ags_vals


@celery.task()
def reducer_task(args):
    """Combine AGS component calculations."""
    categories = args[0]
    ags_dists = args[1]
    result_data = {
        'categories': categories,
        'distributions': ags_dists,
    }
    return result_data


@celery.task(name='ags.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist AGS results."""
    result = AGSResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
