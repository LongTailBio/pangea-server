"""The base Display Module Wrangler module."""

from app.display_modules.utils import jsonify
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup

from .exceptions import EmptyGroupResult


class DisplayModuleWrangler:
    """The base Display Module Wrangler module."""

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather single sample and process."""
        pass

    @classmethod
    def help_run_sample(cls, sample_id, module_name):
        """Gather single sample and process."""
        sample = Sample.objects.get(uuid=sample_id)
        sample.analysis_result.fetch().set_module_status(module_name, 'W')
        return cls.run_sample(sample_id, sample)

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather group of samples and process."""
        pass

    @classmethod
    def help_run_sample_group(cls, sample_group_id, module_name, is_group_tool=False):
        """Gather group of samples and process."""
        sample_group = SampleGroup.query.filter_by(id=sample_group_id).first()

        if not is_group_tool and len(sample_group.sample_ids) <= 1:
            raise EmptyGroupResult()

        samples = jsonify(sample_group.samples)
        sample_group.analysis_result.set_module_status(module_name, 'W')
        return cls.run_sample_group(sample_group, samples)


class SharedWrangler(DisplayModuleWrangler):
    """Base Wrangler for modules with common middleware between Sample and SampleGroup."""

    @classmethod
    def run_common(cls, samples, analysis_result_uuid):
        """Execute common run instructions."""
        raise NotImplementedError('Subclass must override')

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather and process a single sample."""
        samples = [jsonify(sample)]
        analysis_result_uuid = sample.analysis_result.pk

        return cls.run_common(samples, analysis_result_uuid)

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        analysis_result_uuid = sample_group.analysis_result_uuid

        return cls.run_common(samples, analysis_result_uuid)
