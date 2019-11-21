"""Sample model definitions."""

import json
from datetime import datetime
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db


class Sample(db.Model):
    """Represent a sample in the database."""

    __tablename__ = 'samples'
    __table_args__ = (
        UniqueConstraint("library_uuid", "name"),
    )

    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=db.text('uuid_generate_v4()')
    )
    created_at = db.Column(db.DateTime, nullable=False)

    library_uuid = db.Column(
        db.ForeignKey('sample_groups.uuid'),
        nullable=False
    )
    name = db.Column(db.String(256), index=True, nullable=False)
    _sample_metadata = db.Column(db.String(10 * 1000), nullable=True)
    # analysis_results = db.relationship(
    #     'AnalysisResult', backref='sample', lazy=True
    # )
    theme = db.Column(db.String(256), default='')

    def __init__(  # pylint: disable=too-many-arguments
            self, name, library_uuid,
            metadata={},
            created_at=datetime.utcnow()):
        self.library_uuid = library_uuid
        self.name = name
        metadata['name'] = name
        self._sample_metadata = json.dumps(metadata)
        self.created_at = created_at

    def serialize(self):
        pass

    @property
    def sample_metadata(self):
        return json.loads(self._sample_metadata)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
