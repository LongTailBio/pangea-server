"""Sample model definitions."""

import datetime

from uuid import uuid4

from marshmallow import fields
from mongoengine import Document, EmbeddedDocumentField

from app.base import BaseSchema
from app.extensions import mongoDB
from app.tool_results import all_tool_result_modules


class BaseSample(Document):
    """Sample model."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False, default=uuid4)
    name = mongoDB.StringField(unique=True)
    metadata = mongoDB.DictField(default={})
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'allow_inheritance': True}

    @property
    def tool_result_names(self):
        """Return a list of all tool results present for this Sample."""
        blacklist = ['uuid', 'name', 'metadata', 'created_at']
        all_fields = [k
                      for k, v in vars(self).items()
                      if k not in blacklist and not k.startswith('_')]
        return [field for field in all_fields if getattr(self, field, None) is not None]


# Create actual Sample class based on modules present at runtime
Sample = type('Sample', (BaseSample,), {
    module.name(): EmbeddedDocumentField(module.result_model())
    for module in all_tool_result_modules})


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
    created_at = fields.Date()


sample_schema = SampleSchema()   # pylint: disable=invalid-name
