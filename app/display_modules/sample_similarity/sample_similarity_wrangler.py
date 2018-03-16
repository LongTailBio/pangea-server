"""Tasks for generating Sample Similarity results."""

from celery import group

from app.analysis_results.analysis_result_models import AnalysisResultWrapper
from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.sample_similarity.constants import MODULE_NAME
from app.display_modules.sample_similarity.sample_similarity_tasks import (
    taxa_tool_tsne,
    sample_similarity_reducer,
)
from app.display_modules.utils import categories_from_metadata, persist_result
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results.kraken import KrakenResultModule
from app.tool_results.metaphlan2 import Metaphlan2ResultModule


class SampleSimilarityWrangler(DisplayModuleWrangler):
    """Task for generating Reads Classified results."""

    categories_task = categories_from_metadata.s()
    kraken_task = taxa_tool_tsne.s(KrakenResultModule.name())
    metaphlan2_task = taxa_tool_tsne.s(Metaphlan2ResultModule.name())

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather samples and process."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()

        # Set state on Analysis Group
        analysis_group = sample_group.analysis_result
        wrapper = AnalysisResultWrapper(status='W')
        setattr(analysis_group, MODULE_NAME, wrapper)

        persist_task = persist_result.s(analysis_group.uuid, MODULE_NAME)

        middle_tasks = [cls.categories_task, cls.kraken_task, cls.metaphlan2_task]
        tsne_chain = (group(middle_tasks) | sample_similarity_reducer.s() | persist_task)
        result = tsne_chain(sample_group.samples)

        return result
