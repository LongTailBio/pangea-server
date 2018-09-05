"""Tasks for generating Sample Similarity results."""

from celery import chord

from tool_packages.kraken import KrakenResultModule
from tool_packages.krakenhll import KrakenHLLResultModule
from tool_packages.metaphlan2 import Metaphlan2ResultModule

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import categories_from_metadata

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
