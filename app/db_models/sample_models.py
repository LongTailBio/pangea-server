"""Sample model definitions."""

import json
from datetime import datetime
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db

from .analysis_result_models import SampleAnalysisResult


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
    analysis_results = db.relationship(
        'SampleAnalysisResult', backref='parent', lazy=True
    )
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

    def serializable(self):
        out = {
            'sample': {
                'uuid': self.uuid,
                'name': self.name,
                'library_uuid': self.library_uuid,
                'created_at': self.created_at,
                'analysis_result_uuids': [ar.uuid for ar in self.analysis_results],
                'analysis_result_names': [ar.module_name for ar in self.analysis_results],
            },
            'sample_metadata': self.sample_metadata,
        }
        return out

    def serialize(self):
        return json.dumps(self.serializable())

    def analysis_result(self, module_name):
        """Return an AR for the module bound to this sample.

        Create and save the AR if it does not already exist.
        """
        ars = [ar for ar in self.analysis_results if ar.module_name == module_name]
        if ars:
            result = ars[0]
        else:
            result = SampleAnalysisResult(module_name, self.uuid).save()
        return result

    def set_sample_metadata(self, data):
        metadata = self.sample_metadata
        metadata.update(data)
        self._sample_metadata = json.dumps(metadata)
        return self.save()

    @property
    def sample_metadata(self):
        return json.loads(self._sample_metadata)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def from_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).one()

    @classmethod
    def from_name_library(cls, module_name, library_uuid):
        return cls.query.filter_by(library_uuid=library_uuid, name=module_name).one()
