"""AnalysisModule classes."""

from .exceptions import UnsupportedAnalysisMode


class AnalysisModule:
    """
    Base AnalysisModule class.

    AnalysisModules take ToolResult data as input and perform additional analysis.
    """

    @staticmethod
    def name():
        """Return module's unique identifier string."""
        raise NotImplementedError()

    @staticmethod
    def result_model():
        """Return data model class for AnalysisModule type."""
        raise NotImplementedError()

    @staticmethod
    def required_modules():
        """List which analysis modules must be complete for this module to run."""
        return []

    @classmethod
    def is_dependent_on_tool(cls, tool_result_cls):
        """Return True if this AnalysisModule is dependent on a given Tool Result type."""
        required_tools = cls.required_tool_results()
        return tool_result_cls in required_tools

    @staticmethod
    def transmission_hooks():
        """Return a list of hooks to run before transmission to the client."""
        return []

    @staticmethod
    def single_sample_processor():
        """
        Return function(sample_data) for proccessing sample data.

        Where sample_data is a dictionary dump of a single Sample with appropriate ToolResults.

        It is up to the returned function to check the length of *sample_data to see if
        it was called to process a Sample or a SampleGroup and raise a UnsupportedAnalysisMode
        exception where appropriate.
        """
        raise UnsupportedAnalysisMode

    @staticmethod
    def samples_processor():
        """
        Return function(sample_data) for proccessing sample data.

        Where sample_data is one or more dictionary dumps (with appropriate ToolResults)
        of all Samples in a SampleGroup.

        It is up to the returned function to check the length of sample_data to see if
        it was called with an appropriate number of Samples and raise an EmptyGroupResult
        exception where appropriate.
        """
        raise UnsupportedAnalysisMode

    @staticmethod
    def group_tool_processor():
        """
        Return function(group_tool_result) for proccessing a AnalysisModule.

        Ex. Ancestry, Beta Diversity
        """
        raise UnsupportedAnalysisMode
