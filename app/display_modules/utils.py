"""Display module utilities."""

from pprint import pformat

from mongoengine import QuerySet
from mongoengine.errors import ValidationError

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.extensions import celery, celery_logger


def jsonify(mongo_doc):
    """Convert Mongo document to JSON for serialization."""
    if isinstance(mongo_doc, (QuerySet, list,)):
        return [jsonify(element) for element in mongo_doc]
    return mongo_doc.to_mongo().to_dict()


def persist_result_helper(result, analysis_result_id, result_name):
    """Persist results to an Analysis Result model."""
    analysis_result = AnalysisResultMeta.objects.get(uuid=analysis_result_id)
    wrapper = getattr(analysis_result, result_name)
    try:
        wrapper.data = result
        wrapper.status = 'S'
        analysis_result.save()
    except ValidationError:
        contents = pformat(jsonify(result))
        celery_logger.exception(f'Could not save result with contents:\n{contents}')

        wrapper.data = None
        wrapper.status = 'E'
        analysis_result.save()


@celery.task()
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
            categories[prop].add(metadata[prop])

    # Filter for minimum number of values
    categories = {category_name: list(category_values)
                  for category_name, category_values in categories.items()
                  if len(category_values) >= min_size}

    return categories


@celery.task()
def collate_samples(tool_name, fields, samples):
    """Group a set of Tool Result fields from a set of samples by sample name."""
    sample_dict = {}
    for sample in samples:
        sample_name = sample['name']
        sample_dict[sample_name] = {}
        tool_result = sample[tool_name]
        for field in fields:
            sample_dict[sample_name][field] = tool_result[field]

    return sample_dict
