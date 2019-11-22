"""Sample Group model definitions."""

import datetime

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
    owner_uuid = db.Column(UUID(as_uuid=True), index=True, nullable=False)
    owner_name = db.Column(db.String(128), index=True, nullable=False)
    description = db.Column(db.String(300), nullable=False, default='')
    is_library = db.Column(db.Boolean, default=False, nullable=False)
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    samples = db.relationship('Sample', lazy=True)
    analysis_results = db.relationship('GroupAnalysisResult', backref='parent', lazy=True)

    # Duplicate owner properties/indices because we don't know how we will be looking it up
    __table_args__ = (
        db.Index('_sample_group_lower_name_idx',
                 func.lower(name), unique=True),
        db.Index('_sample_group_unique_owner_name_idx',
                 func.lower(name), func.lower(owner_name), unique=True),
        db.Index('_sample_group_unique_owner_uuid_idx',
                 func.lower(name), owner_uuid, unique=True),
    )

    def __init__(  # pylint: disable=too-many-arguments
            self, name, owner_uuid, owner_name,
            description='', is_library=False, is_public=True,
            created_at=datetime.datetime.utcnow()):
        """Initialize MetaGenScope User model."""
        self.name = name
        self.owner_name = owner_name
        self.owner_uuid = owner_uuid
        self.description = description
        self.is_library = is_library
        self.is_public = is_public
        self.created_at = created_at

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

    # @property
    # def samples(self):
    #     """Get SampleGroup's associated Samples.
    #     """
    #     return Sample.quer(uuid__in=self.sample_uuids)

    # @samples.setter
    # def samples(self, value):
    #     """Set SampleGroup's samples."""
    #     self.sample_uuids = [sample.uuid for sample in value]

    # @samples.deleter
    # def samples(self):
    #     """Remove SampleGroup's samples."""
    #     self.sample_uuids = []

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

    def serialize(self):
        pass
