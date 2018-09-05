"""Base AnalysisModule classes."""


DEFAULT_MINIMUM_SAMPLE_COUNT = 2


class AnalysisModule:
    """Base AnalysisModule class."""

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        raise NotImplementedError()

    @classmethod
    def get_result_model(cls):
        """Return data model for AnalysisModule type."""
        raise NotImplementedError()

    @classmethod
    def get_wrangler(cls):
        """Return middleware wrangler for AnalysisModule type."""
        raise NotImplementedError()

    @staticmethod
    def required_tool_results():
        """Enumerate which ToolResult modules a sample must have for this task to run."""
        raise NotImplementedError()

    @classmethod
    def transmission_hooks(cls):
        """Return a list of hooks to run before transmission to the client."""
        return []

    @classmethod
    def is_dependent_on_tool(cls, tool_result_cls):
        """Return True if this AnalysisModule is dependent on a given Tool Result type."""
        required_tools = cls.required_tool_results()
        return tool_result_cls in required_tools

    @classmethod
    def get_data(cls, my_query_result):
        """Transform my_query_result to data."""
        return my_query_result


class SampleToolAnalysisModule(AnalysisModule):  # pylint: disable=abstract-method
    """AnalysisModule dependent on single-sample tool results."""

    @classmethod
    def minimum_samples(cls):
        """Return middleware wrangler for AnalysisModule type."""
        return DEFAULT_MINIMUM_SAMPLE_COUNT


class GroupToolAnalysisModule(AnalysisModule):  # pylint: disable=abstract-method
    """AnalysisModule dependent on a sample group tool result (ex. ancestry, beta diversity)."""

    pass
