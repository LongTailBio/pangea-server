"""Tasks for generating Microbe Directory results."""

from pandas import DataFrame

from tool_packages.microbe_directory import (
    MicrobeDirectoryToolResult,
    MicrobeDirectoryResultModule,
)


def collate_microbe_directory(samples):
    """Collate a group of microbe directory results and fill in blanks."""
    tool_name = MicrobeDirectoryResultModule.name()
    fields = list(MicrobeDirectoryToolResult._fields.keys())  # pylint:disable=no-member
    fields = [field for field in fields if not field == 'id']
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


def processor(*samples):
    """Handle Microbe Directory component calculations."""
    samples = list(samples)
    collated_data = collate_microbe_directory(samples)
    return {'samples': collated_data}
