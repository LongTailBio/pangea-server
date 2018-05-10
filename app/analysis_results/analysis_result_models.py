"""Analysis Results model definitions."""

import datetime
from uuid import uuid4

from marshmallow import fields
from mongoengine import LazyReferenceField

from app.base import BaseSchema
from app.extensions import mongoDB

from .constants import ALL_MODULE_NAMES


ANALYSIS_RESULT_STATUS = (('E', 'ERROR'),
                          ('P', 'PENDING'),
                          ('W', 'WORKING'),
                          ('S', 'SUCCESS'))


class AnalysisResultWrapper(mongoDB.Document):   # pylint: disable=too-few-public-methods
    """Base mongo result class."""

    status = mongoDB.StringField(required=True,
                                 max_length=1,
                                 choices=ANALYSIS_RESULT_STATUS,
                                 default='P')
    data = mongoDB.GenericEmbeddedDocumentField()


class AnalysisResultMetaBase(mongoDB.Document):
    """Base mongo result class."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False, default=uuid4)
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    meta = {'allow_inheritance': True}

    @property
    def result_types(self):
        """Return a list of all analysis result types available for this record."""
        meta_fields = ['uuid', 'created_at', 'meta']
        fields = [field for field in self._fields.keys()  # pylint:disable=no-member
                  if field not in meta_fields
                  and not field.startswith('_')]
        return [field for field in fields
                if getattr(self, field, None) is not None]

    def set_module_status(self, module_name, status):
        """Set the status for a sample group's display module."""
        try:
            wrapper = getattr(self, module_name).fetch()
            wrapper.status = status
            wrapper.save()
        except AttributeError:
            wrapper = AnalysisResultWrapper(status=status).save()
            setattr(self, module_name, wrapper)
        finally:
            self.save()


# Create actual AnalysisResultMeta class based on modules present at runtime
AnalysisResultMeta = type('AnalysisResultMeta', (AnalysisResultMetaBase,), {
    module_name: LazyReferenceField(AnalysisResultWrapper)
    for module_name in ALL_MODULE_NAMES})


class AnalysisResultMetaSchema(BaseSchema):
    """Serializer for AnalysisResultMeta model."""

    __envelope__ = {
        'single': 'analysis_result',
        'many': 'analysis_results',
    }
    __model__ = AnalysisResultMeta

    uuid = fields.Str()
    result_types = fields.List(fields.Str())
    created_at = fields.Date()


analysis_result_schema = AnalysisResultMetaSchema()   # pylint: disable=invalid-name
