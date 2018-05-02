# pylint: disable=too-few-public-methods

"""Factory for generating Analysis Result models for testing."""

import random

import factory

from app.analysis_results.analysis_result_models import AnalysisResultWrapper
from app.display_modules.sample_similarity import (
    ToolDocument,
    SampleSimilarityResult,
)
from app.analysis_results.analysis_result_models import AnalysisResultMeta


class ToolFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Sample Similarity's tool."""

    class Meta:
        """Factory metadata."""

        model = ToolDocument

    x_label = factory.Faker('word').generate({})
    y_label = factory.Faker('word').generate({})


class SampleSimilarityFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Sample Similarity."""

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
    def data_records(self):
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


class SampleSimilarityWrapperFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Sample Similarity status wrapper."""

    class Meta:
        """Factory metadata."""

        model = AnalysisResultWrapper

    status = 'P'
    data = None

    class Params:
        """Factory creation parameters."""

        processed = factory.Trait(
            status='S',
            data=factory.SubFactory(SampleSimilarityFactory)
        )


class AnalysisResultMetaFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result meta."""

    class Meta:
        """Factory metadata."""

        model = AnalysisResultMeta

    sample_similarity = factory.SubFactory(SampleSimilarityWrapperFactory)

    class Params:
        """Factory creation parameters."""

        processed = factory.Trait(
            sample_similarity=factory.SubFactory(SampleSimilarityWrapperFactory, processed=True)
        )
