"""CARD Genes module."""

from app.display_modules.display_module import DisplayModule
from app.tool_results.card_amrs import CARDAMRResultModule

from .models import CARDGenesResult, CARDGenesSampleDocument
from .wrangler import CARDGenesWrangler
from .constants import MODULE_NAME


class CARDGenesDisplayModule(DisplayModule):
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
