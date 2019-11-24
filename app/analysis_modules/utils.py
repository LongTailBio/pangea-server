"""Utilities for the Conductor module."""

from uuid import UUID
from pprint import pformat
from time import sleep

from flask import current_app
from mongoengine.errors import ValidationError

from pangea_modules.base.exceptions import UnsupportedAnalysisMode

from app.analysis_modules import all_analysis_modules, MODULES_BY_NAME
from app.db_models import SampleAnalysisResult, SampleGroup, Sample
from app.extensions import celery, celery_logger, persist_result_lock
from app.utils import lock_function

BLOCK_TIME = 100  # measured in seconds


def apply_errback(signatures):
    """Add error callback to list of signatures."""
    return [sig for sig in signatures if sig is not None]


def fetch_samples(sample_group_id):
    """Get all samples belonging to the specified Sample Group."""
    sample_group = SampleGroup.filter_by(uuid=sample_group_id).one()
    samples = sample_group.samples
    return samples


def filter_samples(samples, module):
    """Filter list of samples to only those supporting the given module."""
    dependencies = {upstream.name() for upstream in module.required_modules()}

    def test_sample(sample):
        """Return true if a sample has all upstreams required by the module."""
        analysis_result = sample.analysis_result.fetch()
        tools_present = set(analysis_result.result_types)
        is_valid = dependencies <= tools_present
        current_app.logger.debug(f'Testing sample: {sample.name}')
        current_app.logger.debug(f'Tools present: {tools_present}')
        current_app.logger.debug(f'Is valid: {is_valid}')
        return is_valid

    result = [sample for sample in samples if test_sample(sample)]
    current_app.logger.debug(f'result: {result}')
    return result


def sample_group_middleware(sample_group_id, *module_names):
    """
    Gather task signatures for sample group.

    *module_names are analysis module names. If not provided, all analysis modules will be run.
    """
    if not module_names:
        module_names = list(MODULES_BY_NAME.keys())
    modules = all_analysis_modules
    if module_names:
        # Raises KeyError for unrecognized module names
        modules = [MODULES_BY_NAME[module_name] for module_name in module_names]

    task_signatures = [module.group_signature(sample_group_id) for module in modules]
    task_signatures = apply_errback(task_signatures)
    return task_signatures


def processes_sample_groups(module_name):
    """Return true if a module processes SampleGroups."""
    analysis_module = MODULES_BY_NAME[module_name]
    try:
        # pylint: disable=assignment-from-no-return
        _ = analysis_module.samples_processor()
        return True
    except UnsupportedAnalysisMode:
        return False


def processes_single_samples(module_name):
    """Return true if a module processes single Samples."""
    analysis_module = MODULES_BY_NAME[module_name]
    try:
        # pylint: disable=assignment-from-no-return
        _ = analysis_module.single_sample_processor()
        return True
    except UnsupportedAnalysisMode:
        return False
