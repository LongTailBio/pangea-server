"""The base Display Module Wrangler module."""


class DisplayModuleWrangler:
    """The base Display Module Wrangler module."""

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather single sample and process."""
        pass

    @classmethod
    def help_run_sample(cls, sample, module):
        """Gather single sample and process."""
        sample.analysis_result.fetch().set_module_status(module.name(), 'W')
        tool_names = [tool.name() for tool in module.required_tool_results()]
        safe_sample = sample.fetch_safe(tool_names)
        return cls.run_sample(sample.uuid, safe_sample)

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather group of samples and process."""
        pass

    @classmethod
    def help_run_sample_group(cls, sample_group, samples, module):
        """Gather group of samples and process."""
        sample_group.analysis_result.set_module_status(module.name(), 'W')
        tool_names = [tool.name() for tool in module.required_tool_results()]
        safe_samples = [sample.fetch_safe(tool_names) for sample in samples]
        return cls.run_sample_group(sample_group, safe_samples)


class SharedWrangler(DisplayModuleWrangler):
    """Base Wrangler for modules with common middleware between Sample and SampleGroup."""

    @classmethod
    def run_common(cls, samples, analysis_result_uuid):
        """Execute common run instructions."""
        raise NotImplementedError('Subclass must override')

    @classmethod
    def run_sample(cls, sample_id, sample):
        """Gather and process a single sample."""
        analysis_result_uuid = sample['analysis_result']

        return cls.run_common([sample], analysis_result_uuid)

    @classmethod
    def run_sample_group(cls, sample_group, samples):
        """Gather and process samples."""
        analysis_result_uuid = sample_group.analysis_result_uuid

        return cls.run_common(samples, analysis_result_uuid)
