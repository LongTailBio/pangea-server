"""Tasks to process Ancestry results."""

from pandas import DataFrame

from analysis_packages.base.utils import collate_samples
from analysis_packages.ancestry_data import AncestryToolResult

from .constants import TOOL_MODULE_NAME


def processor(*samples):
    """Handle Ancestry component calculations."""
    fields = list(AncestryToolResult._fields.keys())  # pylint:disable=no-member
    collate_fields = [field for field in fields if not field == 'id']
    print(samples)
    samples = collate_samples(TOOL_MODULE_NAME, collate_fields, samples)
    print(samples)
    framed_samples = DataFrame(samples).fillna(0).to_dict()
    result = {'samples': framed_samples}
    return result
