"""CARD Genes module."""

from tool_packages.card_amrs import CARDAMRResultModule

from app.display_modules.display_module import SampleToolDisplayModule

from .models import CARDGenesResult, CARDGenesSampleDocument
from .wrangler import CARDGenesWrangler
from .constants import MODULE_NAME


class CARDGenesDisplayModule(SampleToolDisplayModule):
    """CARD Genes factors display module."""

    @staticmethod
    def required_tool_results():
        """Return a list of the necessary result modules."""
        return [CARDAMRResultModule]

    @classmethod
    def name(cls):
        """Return the name of the module."""
        return MODULE_NAME

    @classmethod
    def get_result_model(cls):
        """Return the embedded result."""
        return CARDGenesResult

    @classmethod
    def get_wrangler(cls):
        """Return the wrangler class."""
        return CARDGenesWrangler
