"""Tasks for generating Sample Similarity results."""

from celery import chord

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import categories_from_metadata
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.krakenhll import KrakenHLLResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule

from .tasks import taxa_tool_tsne, sample_similarity_reducer, persist_result


class SampleSimilarityWrangler(DisplayModuleWrangler):
    """Task for generating Reads Classified results."""

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather samples and process."""
        reducer = sample_similarity_reducer.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid)

        categories_task = categories_from_metadata.s(samples)
        kraken_task = taxa_tool_tsne.s(samples, KrakenResultModule.name())
        krakenhll_task = taxa_tool_tsne.s(samples, KrakenHLLResultModule.name())
        metaphlan2_task = taxa_tool_tsne.s(samples, Metaphlan2ResultModule.name())
        middle_tasks = [categories_task, kraken_task, krakenhll_task, metaphlan2_task]

        return chord(middle_tasks)(reducer | persist_task)
