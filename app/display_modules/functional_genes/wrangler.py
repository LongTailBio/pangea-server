"""Tasks for generating Functional Genes results."""

from app.extensions import celery
from app.display_modules.generic_gene_set.wrangler import GenericGeneWrangler
from app.display_modules.utils import persist_result_helper

from .models import FunctionalGenesResult
from .constants import MODULE_NAME, TOP_N, TOOL_MODULE_NAME


@celery.task(name='functional_genes.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Functional Genes results."""
    result = FunctionalGenesResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)


class FunctionalGenesWrangler(GenericGeneWrangler):
    """Tasks for generating virulence results."""

    tool_result_name = TOOL_MODULE_NAME
    result_name = MODULE_NAME

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather single sample and process."""
        func_result = cls.help_run_generic_sample(sample, TOP_N, persist_result)
        return func_result

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        result = cls.help_run_generic_gene_group(sample_group, samples, TOP_N, persist_result)
        return result
