"""Handle loading data from JSON files."""

import json
import os

from analysis_packages.hmp.models import HMPResult
from analysis_packages.reads_classified.models import ReadsClassifiedResult
from analysis_packages.sample_similarity.models import SampleSimilarityResult
from analysis_packages.taxon_abundance.models import TaxonAbundanceResult
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


def load_taxon_abundance():
    """Load Taxon Abundance source JSON."""
    def transform_node(node):
        """Transform JSON node to expected type."""
        return {
            'id': node['id'],
            'name': node['nodeName'],
            'value': node['nodeValue'],
            'rank': 'somerank',
        }

    filename = os.path.join(LOCATION, 'taxaflow.json')
    with open(filename, 'r') as source:
        datastore = json.load(source)['payload']['metaphlan2']
        nodes = [item for sublist in datastore['times'] for item in sublist]
        cleaned_datastore = {
            'nodes': [transform_node(node) for node in nodes],
            'edges': datastore['links']
        }
        result = TaxonAbundanceResult(**{
            'by_tool': {
                'kraken': cleaned_datastore,
                'metaphlan2': cleaned_datastore,
            }
        })
        return result


def load_reads_classified():
    """Load Reads Classified source JSON."""
    def transform_datum(datum):
        """Transform JSON datum to expected type."""
        return {'category': datum['name'], 'values': datum['data']}

    filename = os.path.join(LOCATION, 'reads-classified_col.json')
    with open(filename, 'r') as source:
        datastore = json.load(source)['payload']
        categories = datastore['categories']
        sample_names = datastore['samples']
        data = [transform_datum(datum) for datum in datastore['main']]
        result = ReadsClassifiedResult(categories=categories,
                                       sample_names=sample_names,
                                       data=data)
        return result


def load_hmp():
    """Load HMP source JSON."""
    filename = os.path.join(LOCATION, 'hmp_box.json')
    with open(filename, 'r') as source:
        datastore = json.load(source)['payload']
        categories = datastore['cats2vals']
        sites = datastore['sites']
        data = {category: datastore[category] for category in categories}
        result = HMPResult(categories=categories,
                           sites=sites,
                           data=data)
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
