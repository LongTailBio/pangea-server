"""Create and save a Sample Group with all the fixings (plus gravy)."""

from random import choice
from uuid import uuid4

from pangea_modules.ags.factory import AGSFactory
from pangea_modules.sample_similarity.factory import SampleSimilarityFactory

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.sample_groups.sample_group_models import SampleGroup


def generate_metadata():
    """Generate pseduo-random metadata."""
    result = {
        'location': choice(['house', 'car', 'subway', 'treehouse']),
        'color': choice(['red', 'green', 'blue']),
        'time': choice(['morning', 'evening', 'afternoon', 'night']),
    }
    return result


def wrap_result(result):
    """Wrap display result in status wrapper."""
    return AnalysisResultWrapper(status='S', data=result).save()


def create_saved_group(owner, uuid=None):
    """Create and save a Sample Group with all the fixings (plus gravy)."""
    if uuid is None:
        uuid = uuid4()
    analysis_result = AnalysisResultMeta().save()
    group_description = 'Includes factory-produced analysis results from all display_modules'
    sample_group = SampleGroup(name='Fuzz Testing',
                               owner_uuid=owner.uuid,
                               owner_name=owner.username,
                               is_library=True,
                               analysis_result=analysis_result,
                               description=group_description)
    sample_group.uuid = uuid
    db.session.add(sample_group)
    db.session.commit()

    # Add the results
    analysis_result.average_genome_size = wrap_result(AGSFactory())
    analysis_result.sample_similarity = wrap_result(SampleSimilarityFactory())
    analysis_result.save()

    return sample_group
