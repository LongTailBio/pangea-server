"""Tasks for generating Sample Similarity results."""

import numpy as np
from sklearn.manifold import TSNE

from app.extensions import celery
from app.display_modules.utils import persist_result_helper
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule

from .models import SampleSimilarityResult


def get_clean_samples(sample_dict, no_zero_features=True, zero_threshold=0.00001):
    """
    Clean sample feature data by filling in missing features.

    Parameters
    ----------
    sample_dict : dict
        Dictionary of the form {<sample_id>: <features>}.
    no_zero_features : bool
        If True, features with total value across all samples less than the
        threshold are removed from all samples.
    zero_threshold : float
        The threshold to use for removing features as described above.

    Returns
    -------
    dict
        Cleaned sample set

    """
    # Collect all feature IDs (species names)
    feature_ids = set([])
    for features in sample_dict.values():
        for feature_id in features:
            feature_ids.add(feature_id)
    ordered_feature_ids = list(feature_ids)

    # Fill in missing feature values with 0.0
    samples = {sample_id: {feature_id: features.get(feature_id, 0.0)
                           for feature_id in ordered_feature_ids}
               for sample_id, features in sample_dict.items()}

    # Filter out features with low total
    if no_zero_features:
        # Score all features
        feature_total_score = {feature_id: 0 for feature_id in ordered_feature_ids}
        for features in samples.values():
            for feature_id, value in features.items():
                feature_total_score[feature_id] += value
        # Assign passing grade
        features_passing = {feature_id: value > zero_threshold
                            for feature_id, value in features.items()}

        # Filter features failing to meet threshold from all samples
        samples = {sample_id: {feature_id: value
                               for feature_id, value in features.items()
                               if features_passing[feature_id]}
                   for sample_id, features in samples.items()}

        ordered_feature_ids = [feature_id for feature_id, is_passing
                               in features_passing.items() if is_passing]

    return samples


def run_tsne(samples):
    """Run tSNE algorithm on array of features and return labeled results."""
    feature_array = [[value for value in features.values()]
                     for features in samples.values()]
    feature_array = np.array(feature_array)

    params = {
        'n_components': 2,
        'perplexity': 30.0,
        'early_exaggeration': 2.0,
        'learning_rate': 120.0,
        'n_iter': 1000,
        'min_grad_norm': 1e-05,
        'metric': 'euclidean',
    }
    return TSNE(**params).fit_transform(feature_array)


def label_tsne(tsne_results, sample_names, tool_label):
    """
    Label tSNE results.

    Parameters
    ----------
    tsne_results : np.array
        Output from run_tsne.
    sample_names : list
        List of sample names.
    tool_label : str
        The tool name to use for adding labels.

    Returns
    -------
    dict
        Dictionary of the form: {<sample_name>: <coordinate>}.

    """
    tsne_labeled = {sample_names[i]: {f'{tool_label}_x': float(tsne_results[i][0]),
                                      f'{tool_label}_y': float(tsne_results[i][1])}
                    for i in range(len(sample_names))}
    return tsne_labeled


@celery.task()
def taxa_tool_tsne(samples, tool_name):
    """Run tSNE for tool results stored as 'taxa' property."""
    tool = {
        'x_label': f'{tool_name} tsne x',
        'y_label': f'{tool_name} tsne y',
    }

    sample_dict = {sample['name']: sample[tool_name]['taxa']
                   for sample in samples}
    samples = get_clean_samples(sample_dict)
    taxa_tsne = run_tsne(samples)
    sample_names = list(samples.keys())
    tsne_labeled = label_tsne(taxa_tsne, sample_names, tool_name)

    return (tool, tsne_labeled)


@celery.task()
def sample_similarity_reducer(args, samples):
    """Combine Sample Similarity components."""
    categories = args[0]
    kralen_tool, kraken_labeled = args[1]
    metaphlan_tool, metaphlan_labeled = args[2]

    data_records = []
    for sample in samples:
        sample_id = sample['name']
        data_record = {'SampleID': sample_id}
        data_record.update(kraken_labeled[sample_id])
        data_record.update(metaphlan_labeled[sample_id])
        for category_name in categories.keys():
            category_value = sample['metadata'].get(category_name, 'None')
            data_record[category_name] = category_value
        data_records.append(data_record)

    tools = {
        KrakenResultModule.name(): kralen_tool,
        Metaphlan2ResultModule.name(): metaphlan_tool,
    }

    result_data = {
        'categories': categories,
        'tools': tools,
        'data_records': data_records,
    }
    return result_data


@celery.task(name='sample_similarity.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Sample Similarity results."""
    result = SampleSimilarityResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
