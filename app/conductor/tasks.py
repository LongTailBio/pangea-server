"""Tasks for the Conductor module."""

from app.extensions import celery
from app.sample_groups.sample_group_models import SampleGroup


@celery.task()
def fetch_samples(sample_group_id):
    """Get all samples belonging to the specified Sample Group."""
    sample_group = SampleGroup.query.filter_by(id=sample_group_id).one()
    samples = [sample.fetch_safe() for sample in sample_group.samples]
    return samples
