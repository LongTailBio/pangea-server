"""Factory for generating Multi Axis models for testing."""

from app.display_modules.multi_axis import MultiAxisResult


def create_values():
    return {
        'metaphlan2_taxonomy_profiling': create_metaphlan2(),
        'krakenhll_taxonomy_profiling': create_krakenhll(),
        'align_to_amr_genes': create_card_amr(),
        'humann2_normalize_genes': create_humann2_normalize(),
        'microbe_census': create_microbe_census(),
    }


class MultiAxisFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for Analysis Result's Microbe Directory."""

    class Meta:
        """Factory metadata."""

        model = MultiAxisResult

    @factory.lazy_attribute
    def samples(self):  # pylint: disable=no-self-use
        """Generate random samples."""
        samples = {}
        for i in range(10):
            samples[f'Sample{i}'] = create_values()
        return samples
