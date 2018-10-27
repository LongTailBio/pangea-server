"""Handle loading data from JSON files."""

import json
import os

from analysis_packages.sample_similarity.models import SampleSimilarityResult
from analysis_packages.ags.models import AGSResult


LOCATION = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))


def load_sample_similarity():
    """Load Sample Similarity source JSON."""
    filename = os.path.join(LOCATION, 'sample-similarity_scatter.json')
    with open(filename, 'r') as source:
        datastore = json.load(source)['payload']
        result = SampleSimilarityResult(categories=datastore['categories'],
                                        tools=datastore['tools'],
                                        data_records=datastore['data_records'])
        return result


def load_ags():
    """Load Average Genome source JSON."""
    filename = os.path.join(LOCATION, 'average-genome-size_box.json')
    with open(filename, 'r') as source:
        datastore = json.load(source)['payload']
        categories = datastore['cats2vals']
        distributions = {}
        for category_name, category_values in categories.items():
            distributions[category_name] = {}
            for category_value in category_values:
                raw_data = sorted(datastore[category_name][category_value])
                distribution = {
                    'min_val': raw_data[0],
                    'q1_val': raw_data[1],
                    'mean_val': raw_data[2],
                    'q3_val': raw_data[3],
                    'max_val': raw_data[4],
                }
                distributions[category_name][category_value] = distribution
        result = AGSResult(categories=categories,
                           distributions=distributions)
        return result
