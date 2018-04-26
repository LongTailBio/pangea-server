"""Sample model definitions."""

import datetime

from uuid import uuid4

from marshmallow import fields, pre_dump
from mongoengine import Document, EmbeddedDocumentField

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.base import BaseSchema
from app.extensions import mongoDB
from app.tool_results import all_tool_results
from app.tool_results.modules import SampleToolResultModule


class BaseSample(Document):
    """Sample model."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True,
                             binary=False, default=uuid4)
    name = mongoDB.StringField(unique=True)
    metadata = mongoDB.DictField(default={})
    analysis_result = mongoDB.LazyReferenceField(AnalysisResultMeta)
    theme = mongoDB.StringField(default='')
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'allow_inheritance': True}

    @property
    def tool_result_names(self):
        """Return a list of all tool results present for this Sample."""
        all_fields = [mod.name() for mod in all_tool_results]
        return [field for field in all_fields
                if getattr(self, field, None) is not None]


# Create actual Sample class based on modules present at runtime
Sample = type('Sample', (BaseSample,), {
    module.name(): EmbeddedDocumentField(module.result_model())
    for module in all_tool_results
    if issubclass(module, SampleToolResultModule)})


class SampleSchema(BaseSchema):
    """Serializer for Sample."""

    __envelope__ = {
        'single': 'sample',
        'many': 'samples',
    }
    __model__ = Sample

    uuid = fields.Str()
    name = fields.Str()
    metadata = fields.Dict()
    analysis_result_uuid = fields.Str()
    theme = fields.Str()
    created_at = fields.Date()

    @pre_dump(pass_many=False)
    def add_analysis_result_uuid(self, data):  # pylint: disable=no-self-use
        """Dump analysis_result's UUID."""
        data.analysis_result_uuid = data.analysis_result.pk
        return data


sample_schema = SampleSchema()   # pylint: disable=invalid-name
