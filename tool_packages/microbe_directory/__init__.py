"""Microbe Directory tool module."""

from mongoengine import DynamicField

from tool_packages.base import SampleToolResultModule
from tool_packages.base.models import ToolResult


class MicrobeDirectoryToolResult(ToolResult):     # pylint: disable=too-few-public-methods
    """Microbe Directory result type."""

    # Accept any JSON
    antimicrobial_susceptibility = DynamicField(required=True)
    plant_pathogen = DynamicField(required=True)
    optimal_temperature = DynamicField(required=True)
    optimal_ph = DynamicField(required=True)
    animal_pathogen = DynamicField(required=True)
    microbiome_location = DynamicField(required=True)
    biofilm_forming = DynamicField(required=True)
    spore_forming = DynamicField(required=True)
    pathogenicity = DynamicField(required=True)
    extreme_environment = DynamicField(required=True)
    gram_stain = DynamicField(required=True)


class MicrobeDirectoryResultModule(SampleToolResultModule):
    """Microbe Directory tool module."""

    @classmethod
    def name(cls):
        """Return Microbe Directory module's unique identifier string."""
        return 'microbe_directory_annotate'

    @classmethod
    def result_model(cls):
        """Return Microbe Directory module's model class."""
        return MicrobeDirectoryToolResult
