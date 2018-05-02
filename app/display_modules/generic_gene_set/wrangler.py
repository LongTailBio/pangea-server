"""Tasks for generating Virulence Factor results."""

from celery import chain

from app.display_modules.display_wrangler import DisplayModuleWrangler

from .tasks import filter_gene_results


class GenericGeneWrangler(DisplayModuleWrangler):
    """Tasks for generating virulence results."""

    tool_result_name = None
    result_name = None

    @classmethod
    def help_run_generic_sample(cls, sample, top_n, persist_task):
        """Gather single sample and process."""
        samples = [sample]
        filter_task = filter_gene_results.s(samples,
                                            cls.tool_result_name,
                                            top_n)
        persist_signature = persist_task.s(sample['analysis_result'],
                                           cls.result_name)
        task_chain = chain(filter_task, persist_signature)
        result = task_chain.delay()
        return result

    @classmethod
    def help_run_generic_gene_group(cls, sample_group, samples, top_n, persist_task):
        """Gather and process samples."""
        analysis_result_uuid = sample_group.analysis_result_uuid
        filter_task = filter_gene_results.s(samples,
                                            cls.tool_result_name,
                                            top_n)
        persist_signature = persist_task.s(analysis_result_uuid, cls.result_name)
        task_chain = chain(filter_task, persist_signature)
        result = task_chain.delay()
        return result
