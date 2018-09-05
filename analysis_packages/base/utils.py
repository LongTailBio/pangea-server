"""Utilities for AnalysisModules."""

from mongoengine import QuerySet
from numpy import percentile


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
