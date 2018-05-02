"""Analysis Results model definitions."""

import datetime
from uuid import uuid4

from marshmallow import fields

from app.base import BaseSchema
from app.extensions import mongoDB


ANALYSIS_RESULT_STATUS = (('E', 'ERROR'),
                          ('P', 'PENDING'),
                          ('W', 'WORKING'),
                          ('S', 'SUCCESS'))


class AnalysisResultWrapper(mongoDB.EmbeddedDocument):   # pylint: disable=too-few-public-methods
    """Base mongo result class."""

    status = mongoDB.StringField(required=True,
                                 max_length=1,
                                 choices=ANALYSIS_RESULT_STATUS,
                                 default='P')
    data = mongoDB.GenericEmbeddedDocumentField()


class AnalysisResultMeta(mongoDB.DynamicDocument):
    """Base mongo result class."""

    uuid = mongoDB.UUIDField(required=True, primary_key=True, binary=False, default=uuid4)
    created_at = mongoDB.DateTimeField(default=datetime.datetime.utcnow)

    @property
    def result_types(self):
        """Return a list of all analysis result types available for this record."""
        blacklist = ['uuid', 'created_at']
        all_fields = [k
                      for k, v in vars(self).items()
                      if k not in blacklist and not k.startswith('_')]
        return [field for field in all_fields if hasattr(self, field)]

    def set_module_status(self, module_name, status):
        """Set the status for a sample group's display module."""
        try:
            wrapper = getattr(self, module_name)
            wrapper.status = status
        except AttributeError:
            wrapper = AnalysisResultWrapper(status=status)
            setattr(self, module_name, wrapper)
        finally:
            self.save()


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
