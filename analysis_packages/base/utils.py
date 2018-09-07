"""Utilities for AnalysisModules."""

import inspect

from mongoengine import QuerySet
from numpy import percentile

from .modules import AnalysisModule


def get_primary_module(package):
    """Extract AnalysisModule primary module from package."""
    def test_submodule(submodule):
        """Test a submodule to see if it is an AnalysisModule module."""
        is_correct_subclass = issubclass(submodule, AnalysisModule)
        # Ensure submodule is defined within the package we are inspecting (and not 'base')
        is_correct_module = package.__name__ in submodule.__module__
        return is_correct_subclass and is_correct_module

    submodules = inspect.getmembers(package, inspect.isclass)
    module = next(submodule for _, submodule in submodules
                  if test_submodule(submodule))
    return module

def scrub_object(obj):
    """Remove protected fields from object (dict or list)."""
    if isinstance(obj, list):
        return [scrub_object(item) for item in obj]
    elif isinstance(obj, dict):
        clean_dict = {key: scrub_object(value)
                      for key, value in obj.items()
                      if not key.startswith('_')}
        return clean_dict
    return obj


def jsonify(mongo_doc):
    """Convert Mongo document to JSON for serialization."""
    if isinstance(mongo_doc, (QuerySet, list,)):
        return [jsonify(element) for element in mongo_doc]
    result_dict = mongo_doc.to_mongo().to_dict()
    clean_dict = scrub_object(result_dict)
    return clean_dict


def boxplot(values):
    """Calculate percentiles needed for a boxplot."""
    percentiles = percentile(values, [0, 25, 50, 75, 100])
    result = {'min_val': percentiles[0],
              'q1_val': percentiles[1],
              'mean_val': percentiles[2],
              'q3_val': percentiles[3],
              'max_val': percentiles[4]}
    return result


def scrub_category_val(category_val):
    """Make sure that category val is a string with positive length."""
    if not isinstance(category_val, str):
        category_val = str(category_val)
        if category_val.lower() == 'nan':
            category_val = 'NaN'
    if not category_val:
        category_val = 'NaN'
    return category_val


def collate_samples(tool_name, fields, samples):
    """Group a set of ToolResult fields from a set of samples by sample name."""
    sample_dict = {}
    for sample in samples:
        sample_name = sample['name']
        sample_dict[sample_name] = {}
        tool_result = sample[tool_name]
        for field in fields:
            sample_dict[sample_name][field] = tool_result[field]

    return sample_dict


def categories_from_metadata(samples, min_size=2):
    """
    Create dict of categories and their values from sample metadata.

    Parameters
    ----------
    samples : list
        List of sample models.
    min_size: int
        Minimum number of values required for a given metadata item to
        be included in returned categories.

    Returns
    -------
    dict
        Dictionary of form {<category_name>: [category_value[, category_value]]}

    """
    categories = {}

    # Gather categories and values
    all_metadata = [sample['metadata'] for sample in samples]
    for metadata in all_metadata:
        properties = [prop for prop in metadata.keys()]
        for prop in properties:
            if prop not in categories:
                categories[prop] = set([])
            category_val = metadata[prop]
            category_val = scrub_category_val(category_val)
            categories[prop].add(category_val)

    # Filter for minimum number of values
    categories = {category_name: list(category_values)
                  for category_name, category_values in categories.items()
                  if len(category_values) >= min_size}

    return categories
