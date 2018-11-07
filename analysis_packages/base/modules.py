"""AnalysisModule classes."""

import pandas as pd

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

    @classmethod
    def promote_scalars(cls, samples):
        """Return the promoted form of all scalars as a pandas series."""
        return {
            scalar_var: pd.Series({
                sample['name']: sample[cls.name()][scalar_var]
                for sample in samples
            })
            for scalar_var in cls.result_model().scalar_variables()
        }

    @classmethod
    def promote_vectors(cls, samples, normalize_rows=False, extractor=lambda x: x):
        """Return the promoted form of all vectors as a pandas dataframe."""
        all_vars = {}
        for vector_var in cls.result_model().vector_variables():
            data_tbl = pd.DataFrame.from_dict({
                sample['name']: {
                    feature: extractor(val)
                    for feature, val in sample[cls.name()][vector_var].items()
                }
                for sample in samples
            }, orient='index')
            if normalize_rows:
                data_tbl = data_tbl.div(data_tbl.sum(axis=1), axis=0)
            all_vars[vector_var] = data_tbl
        return all_vars
