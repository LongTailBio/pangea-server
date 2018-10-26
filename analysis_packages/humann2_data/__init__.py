"""HUMANn2 tool module."""

from mongoengine import EmbeddedDocument, EmbeddedDocumentField, FloatField, MapField

from analysis_packages.base import AnalysisModule
from analysis_packages.base.models import ModuleResult

from .constants import MODULE_NAME


class Humann2PathwaysRow(EmbeddedDocument):  # pylint: disable=too-few-public-methods
    """Row for a pathways in humann2."""

    abundance = FloatField()
    coverage = FloatField()


class Humann2Result(ModuleResult):  # pylint: disable=too-few-public-methods
    """HUMANn2 result type."""

    pathways = MapField(field=EmbeddedDocumentField(Humann2PathwaysRow), required=True)


class Humann2ResultModule(AnalysisModule):
    """HUMANn2 tool module."""

    @classmethod
    def name(cls):
        """Return HUMANn2 module's unique identifier string."""
        return MODULE_NAME

    @classmethod
    def result_model(cls):
        """Return HUMANn2 module's model class."""
        return Humann2Result

    @classmethod
    def upload_hooks(cls):
        """Return hook for top level key, pathways."""
        return [lambda payload: {'pathways': payload}]
