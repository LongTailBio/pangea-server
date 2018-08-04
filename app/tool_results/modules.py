"""Base module for Group Tool Results."""

import pandas as pd
from app.extensions import mongoDB


class BaseToolResultModule:
    """Base module for Group Tool Results."""

    @classmethod
    def name(cls):
        """Return Tool Result module's unique identifier string."""
        raise NotImplementedError('ToolResultModule subclass must override')

    @classmethod
    def endpoint(cls):
        """Return Tool Result module's API upload endpoint."""
        raise NotImplementedError('ToolResultModule subclass must override')

    @classmethod
    def result_model(cls):
        """Return the Tool Result module's model class."""
        raise NotImplementedError('ToolResultModule subclass must override')

    @classmethod
    def make_result_model(cls, payload):
        """Process uploaded JSON (if necessary) and create result model."""
        result_model_cls = cls.result_model()
        result_model = result_model_cls(**payload)
        return result_model

    @classmethod
    def upload_hooks(cls):
        """Return a list of functions to be called on uploaded json."""
        return []

    @classmethod
    def run_upload_hooks(cls, payload):
        """Run a set of upload hooks on the given payload and return the result."""
        for hook in cls.upload_hooks():
            payload = hook(payload)
        return payload


class SampleToolResultModule(BaseToolResultModule):
    """Base module for Sample Tool Results."""

    @classmethod
    def name(cls):
        """Return Sample Tool Result module's unique identifier string."""
        raise NotImplementedError('SampleToolResultModule subclass must override')

    @classmethod
    def result_model(cls):
        """Return the Sample Tool Result module's model class."""
        raise NotImplementedError('SampleToolResultModule subclass must override')

    @classmethod
    def endpoint(cls):
        """Return Sample Tool Result module's API upload endpoint."""
        return f'/samples/<uuid>/{cls.name()}'

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


class GroupToolResultModule(BaseToolResultModule):
    """Base module for Group Tool Results."""

    @classmethod
    def name(cls):
        """Return Group Tool Result module's unique identifier string."""
        raise NotImplementedError('GroupToolResultModule subclass must override')

    @classmethod
    def result_model(cls):
        """Return the Group Tool Result module's model class."""
        raise NotImplementedError('GroupToolResultModule subclass must override')

    @classmethod
    def endpoint(cls):
        """Return Tool Result module's API upload endpoint."""
        return f'/sample_groups/<uuid>/{cls.name()}'
