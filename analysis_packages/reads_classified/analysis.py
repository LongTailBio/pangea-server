"""Tasks for generating Reads Classified results."""

from analysis_packages.base.utils import collate_samples

from .constants import TOOL_MODULE_NAME


def processor(*samples):
    """Handle Reads Classified component calculations."""
    samples = list(samples)
    collate_fields = ['viral', 'archaeal', 'bacterial', 'host',
                      'nonhost_macrobial', 'fungal', 'nonfungal_eukaryotic',
                      'unknown']
    collated_samples = collate_samples(TOOL_MODULE_NAME, collate_fields, samples)
    return {'samples': collated_samples}
