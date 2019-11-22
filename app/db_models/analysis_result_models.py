"""Analysis Results model definitions."""

import datetime
import json

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db

from .constants import MAX_DATA_FIELD_LENGTH, ANALYSIS_RESULT_STATUSES


class AnalysisResultField(db.Model):
    """Represent a single field of a single result in the database."""
    __abstract__ = True
    kind = 'virtual'

    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    created_at = db.Column(db.DateTime, nullable=False)
    field_name = db.Column(db.String(256), index=True, nullable=False)
    stored_data = db.Column(db.String(MAX_DATA_FIELD_LENGTH), index=False, nullable=False)

    def __init__(  # pylint: disable=too-many-arguments
            self, analysis_result_uuid, field_name,
            data=[],
            created_at=datetime.datetime.utcnow()):
        """Initialize Analysis Result model."""
        self.parent_uuid = analysis_result_uuid
        self.field_name = field_name
        self.stored_data = json.dumps(data)
        self.created_at = created_at

    @property
    def data(self):
        """Return the deserialized data for this field."""
        return json.loads(self.stored_data)

    def set_data(self, data):
        self.stored_data = json.dumps(data)
        return self.save()

    def serializable(self):
        return {
            'analysis_result_field': {
                'uuid': self.uuid,
                'parent_uuid': self.uuid,
                'field_name': self.field_name,
                'created_at': self.created_at,
            },
            'data': self.data,
        }

    def serialize(self):
        return json.dumps(self.serializable())

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class SampleAnalysisResultField(AnalysisResultField):

    __tablename__ = 'sample_analysis_result_fields'
    kind = 'sample'

    sample_analysis_result_uuid = db.Column(
        db.ForeignKey('sample_analysis_results.uuid'),
        nullable=False
    )

    @property
    def parent_uuid(self):
        """Return the uuid of the parent sample."""
        return self.sample_analysis_result_uuid

    @parent_uuid.setter
    def parent_uuid(self, value):
        """Set the value of parent uuid."""
        self.sample_analysis_result_uuid = value


class SampleGroupAnalysisResultField(AnalysisResultField):

    __tablename__ = 'sample_group_analysis_result_fields'
    kind = 'sample_group'

    sample_group_analysis_result_uuid = db.Column(
        db.ForeignKey('sample_group_analysis_results.uuid'),
        nullable=False
    )

    @property
    def parent_uuid(self):
        """Return the uuid of the parent sample."""
        return self.sample_group_analysis_result_uuid

    @parent_uuid.setter
    def parent_uuid(self, value):
        """Set the value of parent uuid."""
        self.sample_group_analysis_result_uuid = value


class AnalysisResult(db.Model):
    """Represent a single field of a single result in the database.

    Example:
        KrakenUniq produces a table of read-classifications and a report.
        These are stored separately as two separate AnalysisResults.
        Both ARs have the same `module_name` (e.g. KrakenUniq)
        Both ARs have the same owner (e.g. sample-123)
        Both ARs have different a `field_name` (e.g. report or read_class).

    `owner_uuid` should reference a group or sample. Whether it is a group
    or sample is determined by `owned_by_group`. This is only enforced in
    code. The reverse (sample->AR or group->AR) is enforced in SQL.

    AR Fields carry a status marker. In principle all fields of an ARs always
    have the same status.
    """
    __abstract__ = True
    kind = 'virtual'

    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    created_at = db.Column(db.DateTime, nullable=False)

    module_name = db.Column(db.String(256), index=True, nullable=False)
    status = db.Column(db.String(16), index=True, nullable=False)

    def __init__(  # pylint: disable=too-many-arguments
            self, module_name, parent_uuid,
            status='PENDING',
            created_at=datetime.datetime.utcnow()):
        """Initialize Analysis Result model."""
        self.module_name = module_name
        self.parent_uuid = parent_uuid
        self.status = status
        self.created_at = created_at

    def field(self, field_name):
        """Return an AR-filed for the module bound to this AR.

        Create and save the AR-field if it does not already exist.
        """
        ar_fs = [ar_f for ar_f in self.module_fields if ar_f.field_name == field_name]
        if ar_fs:
            return ar_fs[0]
        return type(self)._field_type()(self.uuid, field_name).save()

    def set_status(self, status):
        """Set status and save. Return self."""
        assert status in ANALYSIS_RESULT_STATUSES
        self.status = status
        return self.save()

    def serializable(self):
        out = {
            'analysis_result': {
                'uuid': self.uuid,
                'parent_uuid': self.uuid,
                'module_name': self.module_name,
                'kind': self.kind,
                'status': self.status,
                'created_at': self.created_at,
                'fields': {}
            },
            'data': {},
        }
        for field in self.module_fields:
            myfield = field.serializable()
            out['data'][field.field_name] = myfield['data']
            out['analysis_result']['fields'][field.field_name] = myfield['analysis_result_field']
        return out

    def serialize(self):
        return json.dumps(self.serializable())

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class SampleAnalysisResult(AnalysisResult):

    __tablename__ = 'sample_analysis_results'
    __table_args__ = (
        UniqueConstraint("sample_uuid", "module_name"),
    )

    sample_uuid = db.Column(
        db.ForeignKey('samples.uuid'),
        nullable=False
    )
    module_fields = db.relationship(
        'SampleAnalysisResultField', backref='analysis_result', lazy=True
    )
    kind = 'sample'

    @property
    def parent_uuid(self):
        """Return the uuid of the parent sample."""
        return self.sample_uuid

    @parent_uuid.setter
    def parent_uuid(self, value):
        """Set the value of parent uuid."""
        self.sample_uuid = value

    @classmethod
    def _field_type(cls):
        return SampleAnalysisResultField


class SampleGroupAnalysisResult(AnalysisResult):

    __tablename__ = 'sample_group_analysis_results'
    __table_args__ = (
        UniqueConstraint("sample_group_uuid", "module_name"),
    )

    sample_group_uuid = db.Column(
        db.ForeignKey('sample_groups.uuid'),
        nullable=False
    )
    module_fields = db.relationship(
        'SampleGroupAnalysisResultField', backref='analysis_result', lazy=True
    )
    kind = 'sample_group'

    @property
    def parent_uuid(self):
        """Return the uuid of the parent sample."""
        return self.sample_group_uuid

    @parent_uuid.setter
    def parent_uuid(self, value):
        """Set the value of parent uuid."""
        self.sample_group_uuid = value

    @classmethod
    def _field_type(cls):
        return SampleAnalysisResultField
