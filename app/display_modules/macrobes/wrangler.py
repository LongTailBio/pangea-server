"""Wrangler for Macrobe Directory results."""

from celery import chain
from pandas import DataFrame

from app.display_modules.display_wrangler import DisplayModuleWrangler
from app.display_modules.utils import persist_result_helper
from app.extensions import celery
from app.tool_results.macrobes import MacrobeResultModule

from .constants import MODULE_NAME
from .models import MacrobeResult


@celery.task()
def collate_macrobes(samples):
    """Group a macrobes from a set of samples."""
    sample_dict = {}
    for sample in samples:
        sample_name = sample['name']
        sample_dict[sample_name] = {
            macrobe_name: val['rpkm']
            for macrobe_name, val in sample[MacrobeResultModule.name()]['macrobes'].items()
        }
    sample_tbl = DataFrame.from_dict(sample_dict, orient='index').fillna(0)
    sample_tbl = (sample_tbl - sample_tbl.mean()) / sample_tbl.std(ddof=0)  # z score normalize
    return {'samples': sample_tbl.to_dict()}


@celery.task(name='macrobe_abundance.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Macrone results."""
    result = MacrobeResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)


class MacrobeWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather single sample and process."""
        samples = [sample]
        collate_task = collate_macrobes.s(samples)
        persist_task = persist_result.s(sample['analysis_result'], MODULE_NAME)

        task_chain = chain(collate_task, persist_task)
        result = task_chain.delay()

        return result

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        collate_task = collate_macrobes.s(samples)
        persist_task = persist_result.s(sample_group.analysis_result_uuid, MODULE_NAME)

        task_chain = chain(collate_task, persist_task)
        result = task_chain.delay()

        return result
