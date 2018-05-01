"""The Conductor module orchestrates Display module generation based on changing data."""

from flask import current_app

from app.display_modules import all_display_modules, sample_display_modules
from app.display_modules.utils import jsonify
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup
from app.tool_results import all_group_results


class DisplayModuleConductor:
    """The Conductor module orchestrates Display module generation based on ToolResult changes."""

    def __init__(self, display_modules):
        """
        Initialize the Conductor.

        Parameters
        ----------
        display_modules: [DisplayModule]
            The list of DisplayModules to kick off middleware for.

        """
        self.display_modules = display_modules

    @staticmethod
    def downstream_modules(tool_result_cls):
        """Calculate display modules dependent on the provided tool result class."""
        downstream_modules = [module for module in all_display_modules
                              if module.is_dependent_on_tool(tool_result_cls)]
        return downstream_modules

    def shake_that_baton(self):
        """Begin the orchestration of middleware tasks."""
        raise NotImplementedError('Subclass must override.')


class SampleConductor(DisplayModuleConductor):
    """Orchestrates Display Module generation based on SampleToolResult changes."""

    def __init__(self, sample_id, display_modules=sample_display_modules,
                 downstream_groups=True):
        """
        Initialize the Conductor.

        Parameters
        ----------
        sample_id : str
            The ID of the Sample that had a ToolResult change event.
        display_modules: [DisplayModule]
            The list of DisplayModules to kick off middleware for.

        """
        super(SampleConductor, self).__init__(display_modules)

        self.sample_id = sample_id
        self.downstream_groups = downstream_groups

    def get_valid_modules(self, tools_present):
        """
        Determine which dispaly modules can be computed based on tool results present.

        Parameters
        ----------
        tools_present : set<str>
            A set of of tool result names.

        Returns
        -------
        list<DisplayModule>
            A list of all DisplayModules to be recomputed based on the tools present.

        """
        valid_modules = []
        for module in self.display_modules:
            dependencies = set([tool.name() for tool in module.required_tool_results()])
            if dependencies <= tools_present:
                valid_modules.append(module)
        return valid_modules

    def filtered_samples(self, samples, module):  # pylint:disable=no-self-use
        """Filter list of samples to only those supporting the given module."""
        current_app.logger.info('Filtering samples')

        dependencies = set([tool.name() for tool in module.required_tool_results()])

        current_app.logger.info(f'Dependencies: {dependencies}')

        def test_sample(sample):
            """Test a single sample to see if it has all tools required by the display module."""
            current_app.logger.info(f'Testing sample: {sample.name}')
            tools_present = set(sample.tool_result_names)
            current_app.logger.info(f'Tools present: {tools_present}')
            is_valid = dependencies <= tools_present
            current_app.logger.info(f'Is valid: {is_valid}')
            return is_valid

        result = [sample for sample in samples if test_sample(sample)]
        current_app.logger.info(f'result: {result}')
        return result

    def direct_sample_group(self, sample_group):
        """Kick off computation for a sample group's relevant DisplayModules."""
        # Cache samples
        samples = sample_group.samples

        # These should only ever be SampleToolDisplayModule
        for module in self.display_modules:
            module_name = module.name()
            current_app.logger.info(f'Checking module: {module_name}')
            filtered_samples = self.filtered_samples(samples, module)
            if filtered_samples:
                current_app.logger.info(f'Filtered samples: {len(filtered_samples)}')
                # Pass off middleware execution to Wrangler
                module.get_wrangler().help_run_sample_group(sample_group=sample_group,
                                                            samples=filtered_samples,
                                                            module=module)
            else:
                current_app.logger.info(f'Attempted to run {module_name} sample group '
                                        'without at least two samples')

    def direct_sample_groups(self):
        """Kick off computation for affected sample groups' relevant DisplayModules."""
        query_filter = SampleGroup.sample_ids.contains(self.sample_id)
        sample_groups = SampleGroup.query.filter(query_filter)
        for sample_group in sample_groups:
            self.direct_sample_group(sample_group)

    def direct_sample(self, sample):
        """Kick off computation for the affected sample's relevant DisplayModules."""
        tools_present = set(sample.tool_result_names)
        valid_modules = self.get_valid_modules(tools_present)
        for module in valid_modules:
            # Pass off middleware execution to Wrangler
            module.get_wrangler().help_run_sample(sample_id=sample, module=module)

    def shake_that_baton(self):
        """Begin the orchestration of middleware tasks."""
        sample = Sample.objects.get(uuid=self.sample_id)
        self.direct_sample(sample)
        if self.downstream_groups:
            self.direct_sample_groups()


class GroupConductor(DisplayModuleConductor):
    """
    Orchestrates Display Module generation based on changes to a Sample Group.

    This could be:
        - GroupToolResult upload
        - Manual kick-off of a set of display modules for a sample group
    """

    def __init__(self, sample_group_uuid,               # pylint:disable=dangerous-default-value
                 display_modules=all_display_modules):
        """
        Initialize the Conductor.

        Parameters
        ----------
        sample_group_uuid : str
            The ID of the SampleGroup that had a ToolResult change event.
        display_modules: [DisplayModule]
            The list of DisplayModules to kick off middleware for.

        """
        super(GroupConductor, self).__init__(display_modules)

        self.sample_group_uuid = sample_group_uuid

    def filter_modules(self, modules, sample_group):  # pylint:disable=no-self-use
        """Filter modules by whether they are supported by the sample group."""
        def test_tool(tool):
            """Test a single tool to see if it exists for the sample group."""
            model_cls = tool.result_model()
            query = model_cls.objects(sample_group_uuid=sample_group.id)
            result = query.count() > 0
            return result

        group_results_present = set([tool.name() for tool in all_group_results
                                     if test_tool(tool)])

        def test_module(module):
            """Test a single module to see if all required tools are present."""
            dependencies = set([tool.name() for tool in module.required_tool_results()])
            result = dependencies <= group_results_present
            return result

        return [module for module in modules if test_module(module)]

    def direct_sample_group(self, sample_group):
        """Kick off computation for a sample group's relevant DisplayModules."""
        # These should only ever be GroupToolDisplayModule
        filtered_modules = self.filter_modules(self.display_modules, sample_group)
        for module in filtered_modules:
            # Pass off middleware execution to Wrangler
            module.get_wrangler().help_run_sample_group(sample_group=sample_group,
                                                        samples=[],
                                                        module=module)

    def shake_that_baton(self):
        """Begin the orchestration of middleware tasks."""
        sample_group = SampleGroup.objects.get(id=self.sample_group_uuid)
        self.direct_sample_group(sample_group)
