"""Tasks for generating Top Taxa results."""

from celery import chord

from app.display_modules.display_wrangler import DisplayModuleWrangler

from .tasks import find_top_taxa, persist_result


class TopTaxaWrangler(DisplayModuleWrangler):
    """Tasks for generating Top Taxa results."""

    @staticmethod
    def run_sample_group(sample_group, samples):
        """Gather samples then process them."""
        persist_task = persist_result.s(sample_group.analysis_result_uuid)
        top_taxa_task = find_top_taxa.s(samples)

        return chain(top_taxa_task, persist_task).delay()
