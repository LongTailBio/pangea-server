"""Sample Group model definitions."""

import datetime
import json
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID

from app.extensions import db

from .sample_models import Sample
from .analysis_result_models import SampleGroupAnalysisResult


class SampleGroup(db.Model):  # pylint: disable=too-many-instance-attributes
    """MetaGenScope Sample Group model."""

    __tablename__ = 'sample_groups'

    uuid = db.Column(UUID(as_uuid=True),
                     primary_key=True,
                     server_default=db.text('uuid_generate_v4()'))
    name = db.Column(db.String(128), index=True, nullable=False)
    organization_uuid = db.Column(db.ForeignKey('organizations.uuid'), nullable=False)
    description = db.Column(db.String(300), nullable=False, default='')
    is_library = db.Column(db.Boolean, default=False, nullable=False)
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    samples = db.relationship('Sample', lazy=True)
    analysis_results = db.relationship('SampleGroupAnalysisResult', backref='parent', lazy=True)

    # Duplicate owner properties/indices because we don't know how we will be looking it up
    __table_args__ = (
        db.Index('_sample_group_lower_name_idx',
                 func.lower(name), unique=True),
    )

    def __init__(  # pylint: disable=too-many-arguments
            self, name, organization_uuid,
            description='', is_library=False, is_public=True,
            created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope User model."""
        self.name = name
        self.organization_uuid = organization_uuid
        self.description = description
        self.is_library = is_library
        self.is_public = is_public
        self.created_at = created_at

    def sample(self, sample_name, metadata={}, force_new=False):
        """Return a sample bound to this library.

        Create and save the sample if it does not already exist.
        """
        samps = [samp for samp in self.samples if samp.name == sample_name]
        if samps and not force_new:
            return samps[0]
        return Sample(sample_name, self.uuid, metadata=metadata).save()

    def analysis_result(self, module_name):
        """Return an AR for the module bound to this sample.

        Create and save the AR if it does not already exist.
        """
        ars = [ar for ar in self.analysis_results if ar.module_name == module_name]
        if ars:
            result = ars[0]
        else:
            result = SampleGroupAnalysisResult(module_name, self.uuid).save()
        return result

    @property
    def sample_uuids(self):
        return [sample.uuid for sample in self.samples]

    @property
    def tools_present(self):
        """Return list of names for Tool Results present across all Samples in this group."""
        # Cache samples
        samples = self.samples

        tools_present_in_all = set([])
        for i, sample in enumerate(samples):
            tool_results = set(sample.tool_result_names)
            if i == 0:
                tools_present_in_all |= tool_results
            else:
                tools_present_in_all &= tool_results
        return list(tools_present_in_all)

    def serializable(self):
        out = {
            'sample_group': {
                'uuid': self.uuid,
                'name': self.name,
                'organization_uuid': self.organization_uuid,
                'description': self.description,
                'is_library': self.is_library,
                'is_public': self.is_public,
                'created_at': self.created_at,
                'sample_uuids': [sample.uuid for sample in self.samples],
                'sample_names': [sample.name for sample in self.samples],
                'analysis_result_uuids': [ar.uuid for ar in self.analysis_results],
                'analysis_result_names': [ar.module_name for ar in self.analysis_results],
            },
        }
        return out

    def serialize(self):
        return json.dumps(self.serializable())

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def from_uuid(cls, uuid):
        return cls.query.filter_by(uuid=uuid).one()

    @classmethod
    def from_name(cls, name):
        return cls.query.filter_by(name=name).one()
