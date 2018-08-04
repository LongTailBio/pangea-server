"""Factory for generating Sample Similarity models for testing."""

from app.display_modules.sample_similarity import SampleSimilarityResult

CATEGORIES = {
    'city': ['Montevideo', 'Sacramento']
}

TOOLS = {
    'metaphlan2': {
        'x_label': 'metaphlan2 tsne x',
        'y_label': 'metaphlan2 tsne y'
    }
}

DATA_RECORDS = [{
    'SampleID': 'MetaSUB_Pilot__01_cZ__unknown__seq1end',
    'city': 'Montevideo',
    'metaphlan2_x': 0.46118640628005614,
    'metaphlan2_y': 0.15631940943278633,
}]


def create_mvp_sample_similarity():
    """Create the most minimal Sample Similarity model possible."""
    sample_similarity_result = SampleSimilarityResult(categories=CATEGORIES,
                                                      tools=TOOLS,
                                                      data_records=DATA_RECORDS)
    return sample_similarity_result
