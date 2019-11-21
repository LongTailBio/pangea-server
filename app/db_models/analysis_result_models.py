"""Analysis Results model definitions."""

import datetime
import json

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db

from .constants import MAX_DATA_FIELD_LENGTH


class AnalysisResultField(db.Model):
    """Represent a single field of a single result in the database."""

    __tablename__ = 'analysis_result_fields'

    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    created_at = db.Column(db.DateTime, nullable=False)
    analysis_result_uuid = db.Column(
        db.ForeignKey('analysis_results.uuid'),
        nullable=False
    )
    field_name = db.Column(db.String(256), index=True, nullable=False)
    data = db.Column(db.String(MAX_DATA_FIELD_LENGTH), index=True, nullable=False)

    def __init__(  # pylint: disable=too-many-arguments
            self, analysis_result_uuid, field_name,
            data=[],
            owned_by_group=False,
            created_at=datetime.datetime.utcnow()):
        """Initialize Analysis Result model."""
        self.analysis_result_uuid = analysis_result_uuid
        self.field_name = field_name
        self.data = json.dumps(data)
        self.created_at = created_at

    def serialize(self):
        pass


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

    __tablename__ = 'analysis_results'

    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    created_at = db.Column(db.DateTime, nullable=False)

    module_name = db.Column(db.String(256), index=True, nullable=False)
    module_fields = db.relationship(
        'AnalysisResultField', backref='analysis_result', lazy=True
    )

    status = db.Column(db.String(16), index=True, nullable=False)
    owned_by_group = db.Column(db.Boolean, default=False, nullable=False)
    owner_uuid = db.Column(UUID(as_uuid=True), nullable=False)

    def __init__(  # pylint: disable=too-many-arguments
            self, module_name, field_name, status, owner_uuid,
            data=[],
            owned_by_group=False,
            created_at=datetime.datetime.utcnow()):
        """Initialize Analysis Result model."""
        self.module_name = module_name
        self.field_name = field_name
        self.data = json.dumps(data)
        self.status = status
        self.owner_uuid = owner_uuid
        self.owned_by_group = owned_by_group
        self.created_at = created_at

    def serialize(self):
        pass
