"""Tasks for generating Virulence Factor results."""

from app.display_modules.generic_gene_set.wrangler import GenericGeneWrangler

from .models import VFDBResult
from .constants import MODULE_NAME, TOP_N


class VFDBWrangler(GenericGeneWrangler):
    """Tasks for generating virulence results."""

    tool_result_name = 'vfdb_quantify'
    result_name = MODULE_NAME

    @classmethod
    def run_sample_group(cls, sample_group_id):
        """Gather and process samples."""
        result = cls.help_run_sample_group(VFDBResult, TOP_N, sample_group_id)
        return result