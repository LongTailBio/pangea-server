"""Tasks for generating Microbe Directory results."""

from pandas import DataFrame

from app.extensions import celery
from app.display_modules.utils import persist_result_helper
from app.tool_results.microbe_directory import (
    MicrobeDirectoryToolResult,
    MicrobeDirectoryResultModule,
)

from .models import MicrobeDirectoryResult


@celery.task()
def collate_microbe_directory(samples):
    """Collate a group of microbe directory results and fill in blanks."""
    tool_name = MicrobeDirectoryResultModule.name()
    fields = list(MicrobeDirectoryToolResult._fields.keys())
    field_dict = {}
    for field in fields:
        field_dict[field] = {}
        for sample in samples:
            sample_name = sample['name']
            tool_result = sample[tool_name]
            field_dict[field][sample_name] = tool_result[field]
        field_df = DataFrame.from_dict(field_dict[field])
        field_df = field_df.fillna(0)
        field_dict[field] = field_df.to_dict()

    sample_dict = {}
    for sample in samples:
        sample_name = sample['name']
        sample_dict[sample_name] = {}
        for field in fields:
            sample_dict[sample_name][field] = field_dict[field][sample_name]

    return sample_dict


@celery.task()
def microbe_directory_reducer(samples):
    """Wrap collated samples as actual Result type."""
    result_data = {'samples': samples}
    return result_data


@celery.task(name='microbe_directory.persist_result')
def persist_result(result_data, analysis_result_id, result_name):
    """Persist Microbe Directory results."""
    result = MicrobeDirectoryResult(**result_data)
    persist_result_helper(result, analysis_result_id, result_name)
