"""Sample model definitions."""

import datetime

from uuid import uuid4

from marshmallow import fields
from mongoengine import Document

from app.analysis_results.analysis_result_models import AnalysisResultMeta
from app.base import BaseSchema
from app.extensions import mongoDB


class BaseSample(Document):
    """Sample model."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True,
                             binary=False, default=uuid4)
    library_uuid = mongoDB.UUIDField(required=True, binary=False)
    name = mongoDB.StringField(required=True, unique_with='library_uuid')
    metadata = mongoDB.DictField(default={})
    analysis_result = mongoDB.LazyReferenceField(AnalysisResultMeta)
    theme = mongoDB.StringField(default='')
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'allow_inheritance': True}

    def __contains__(self, key):
        """Return true if property is in the class without fetching."""
        try:
            getattr(self, key)
        except KeyError:
            try:
                getattr(self.analysis_result, key)
            except KeyError:
                return False
        return True

    def __getitem__(self, key):
        """Return property of sample or of analysis result."""
        try:
            return getattr(self, key)
        except KeyError:
            return getattr(self.analysis_result, key).fetch()


# Create actual Sample class based on modules present at runtime
Sample = type('Sample', (BaseSample,), {})


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
    analysis_result_uuid = fields.Function(lambda obj: obj.analysis_result.pk)
    theme = fields.Str()
    created_at = fields.Date()


sample_schema = SampleSchema()   # pylint: disable=invalid-name
