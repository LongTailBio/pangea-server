"""Factory for generating Sample Similarity models for testing."""

import factory

from ..models import SampleSimilarityResult

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


class SampleSimilarityFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Sample Similarity."""

    class Meta:
        """Factory metadata."""

        model = SampleSimilarityResult

    @factory.lazy_attribute
    def categories(self):  # pylint: disable=no-self-use
        """Use stock categories."""
        return CATEGORIES

    @factory.lazy_attribute
    def tools(self):  # pylint: disable=no-self-use
        """Use stock tools."""
        return TOOLS

    @factory.lazy_attribute
    def data_records(self):  # pylint: disable=no-self-use
        """Use stock data records."""
        return DATA_RECORDS
