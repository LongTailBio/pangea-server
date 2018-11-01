# pylint: disable=too-few-public-methods

"""Factory for generating Sample Similarity models for testing."""

import random
import factory

from ..models import SampleSimilarityResult, ToolDocument

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


class ToolFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Sample Similarity's tool subdocument."""

    class Meta:
        """Factory metadata."""

        model = ToolDocument

    x_label = factory.Faker('word').generate({})
    y_label = factory.Faker('word').generate({})


class SampleSimilarityFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Sample Similarity."""

    class Meta:
        """Factory metadata."""

        model = SampleSimilarityResult

    @factory.lazy_attribute
    def categories(self):  # pylint: disable=no-self-use
        """Generate categories."""
        category_name = factory.Faker('word').generate({})
        return {category_name: factory.Faker('words', nb=4).generate({})}

    @factory.lazy_attribute
    def tools(self):  # pylint: disable=no-self-use
        """Generate tools."""
        tool_name = factory.Faker('word').generate({})
        return {tool_name: ToolFactory()}

    @factory.lazy_attribute
    def data_records(self):  # pylint: disable=no-self-use
        """Generate data records."""
        name = factory.Faker('company').generate({}).replace(' ', '_')

        def record(i):
            """Generate individual record."""
            result = {'SampleID': f'{name}__seq{i}'}
            for category, category_values in self.categories.items():
                result[category] = random.choice(category_values)

            decimal = factory.Faker('pyfloat', left_digits=0, positive=True)
            for tool in self.tools:
                result[f'{tool}_x'] = decimal.generate({})
                result[f'{tool}_y'] = decimal.generate({})

            return result

        return [record(i) for i in range(20)]
