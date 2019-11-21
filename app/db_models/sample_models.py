"""Sample model definitions."""

import datetime
import json

from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class Sample(db.Model):
    """Represent a sample in the database."""

    __tablename__ = 'samples'

    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    created_at = db.Column(db.DateTime, nullable=False)

    library_uuid = db.Column(
        db.Integer,
        db.ForeignKey('sample_groups.uuid'),
        nullable=False
    )
    name = db.Column(db.String(256), index=True, nullable=False)
    sample_metadata = db.Column(db.String(10 * 1000), nullable=True)
    analysis_results = db.relationship(
        'AnalysisResult', backref='sample', lazy=True
    )
    theme = db.Column(db.String(256), default='')

    def __init__(  # pylint: disable=too-many-arguments
            self, library_uuid, name,
            metadata={},
            created_at=datetime.datetime.utcnow()):
        self.library_uuid = library_uuid
        self.name = name
        self.sample_metadata = json.dumps(metadata)
        self.created_at = created_at

    def serialize(self):
        pass
