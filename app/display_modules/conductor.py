"""The Conductor module orchestrates Display module generation based on changing data."""

from flask import current_app

from app.display_modules import all_display_modules
from app.display_modules.exceptions import EmptyGroupResult
from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup


class DisplayModuleConductor:
    """The Conductor module orchestrates Display module generation based on ToolResult changes."""

    def __init__(self, tool_result_cls):
        """
        Initialize the Conductor.

        Parameters
        ----------
        tool_result_cls: ToolResultModule
            The class of the ToolResult that was changed.

        """
        self.tool_result_cls = tool_result_cls
        self.downstream_modules = [module for module in all_display_modules
                                   if module.is_dependent_on_tool(self.tool_result_cls)]

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
        for module in self.downstream_modules:
            dependencies = set([tool.name() for tool in module.required_tool_results()])
            if dependencies <= tools_present:
                valid_modules.append(module)
        return valid_modules

    def direct_sample(self, sample):
        """Kick off computation for the affected sample's relevant DisplayModules."""
        tools_present = set(sample.tool_result_names)
        valid_modules = self.get_valid_modules(tools_present)
        for module in valid_modules:
            # Pass off middleware execution to Wrangler
            module_name = module.name()
            module.get_wrangler().help_run_sample(sample_id=sample.uuid,
                                                  module_name=module_name)

    def direct_sample_group(self, sample_group, is_group_tool=False):
        """Kick off computation for a sample group's relevant DisplayModules."""
        tools_present_in_all = set(sample_group.tools_present)
        valid_modules = self.get_valid_modules(tools_present_in_all)
        for module in valid_modules:
            # Pass off middleware execution to Wrangler
            module_name = module.name()
            try:
                module.get_wrangler().help_run_sample_group(sample_group_id=sample_group.id,
                                                            module_name=module_name,
                                                            is_group_tool=is_group_tool)
            except EmptyGroupResult:
                current_app.logger.info(f'Attempted to run {module_name} sample group '
                                        'without at least two samples')

    def shake_that_baton(self):
        """Begin the orchestration of middleware tasks."""
        raise NotImplementedError('Subclass must override.')


class SampleConductor(DisplayModuleConductor):
    """Orchestrates Display Module generation based on SampleToolResult changes."""

    def __init__(self, sample_id, tool_result_cls):
        """
        Initialize the Conductor.

        Parameters
        ----------
        sample_id : str
            The ID of the Sample that had a ToolResult change event.
        tool_result_cls: ToolResultModule
            The class of the ToolResult that was changed.

        """
        super(SampleConductor, self).__init__(tool_result_cls)

        self.sample_id = sample_id

    def direct_sample_groups(self):
        """Kick off computation for affected sample groups' relevant DisplayModules."""
        query_filter = SampleGroup.sample_ids.contains(self.sample_id)
        sample_groups = SampleGroup.query.filter(query_filter)
        for sample_group in sample_groups:
            self.direct_sample_group(sample_group)

    def shake_that_baton(self):
        """Begin the orchestration of middleware tasks."""
        sample = Sample.objects.get(uuid=self.sample_id)
        self.direct_sample(sample)
        self.direct_sample_groups()


class GroupConductor(DisplayModuleConductor):
    """Orchestrates Display Module generation based on GroupToolResult changes."""

    def __init__(self, sample_group_uuid, tool_result_cls):
        """
        Initialize the Conductor.

        Parameters
        ----------
        sample_group_uuid : str
            The ID of the SampleGroup that had a ToolResult change event.
        tool_result_cls: ToolResultModule
            The class of the ToolResult that was changed.

        """
        super(GroupConductor, self).__init__(tool_result_cls)

        self.sample_group_uuid = sample_group_uuid

    def shake_that_baton(self):
        """Begin the orchestration of middleware tasks."""
        sample_group = SampleGroup.objects.get(id=self.sample_group_uuid)
        self.direct_sample_group(sample_group, is_group_tool=True)
