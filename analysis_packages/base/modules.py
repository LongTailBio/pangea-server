"""
Base AnalysisModule classes.

AnalysisModules take ToolResult data as input and perform additional analysis.
"""

from .constants import DEFAULT_MINIMUM_SAMPLE_COUNT


class AnalysisModule:
    """Base AnalysisModule class."""

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        raise NotImplementedError()

    @staticmethod
    def result_model():
        """Return data model class for AnalysisModule type."""
        raise NotImplementedError()

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have for this task to run."""
        raise NotImplementedError()

    @staticmethod
    def transmission_hooks():
        """Return a list of hooks to run before transmission to the client."""
        return []

    @classmethod
    def is_dependent_on_tool(cls, tool_result_cls):
        """Return True if this AnalysisModule is dependent on a given Tool Result type."""
        required_tools = cls.required_tool_results()
        return tool_result_cls in required_tools


class SampleToolAnalysisModule(AnalysisModule):  # pylint: disable=abstract-method
    """AnalysisModule dependent on single-sample tool results."""

    @staticmethod
    def processor():
        """
        Return function(*sample_data) for proccessing sample data.

        Where sample_data is one or more dictionary dumps (with appropriate ToolResults)
        of either a single Sample or all Samples in a SampleGroup.

        It is up to the returned function to check the length of *sample_data to see if
        it was called to process a Sample or a SampleGroup and raise a NotImplementedError
        where appropriate.
        """
        raise NotImplementedError()

    @staticmethod
    def minimum_samples():
        """Return middleware wrangler for AnalysisModule type."""
        return DEFAULT_MINIMUM_SAMPLE_COUNT


class GroupToolAnalysisModule(AnalysisModule):  # pylint: disable=abstract-method
    """AnalysisModule dependent on a sample group tool result (ex. Ancestry, Beta Diversity)."""

    @staticmethod
    def processor():
        """Return function(group_tool_result) for proccessing a GroupToolAnalysisModule."""
        raise NotImplementedError()
