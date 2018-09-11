# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

from analysis_packages.generic_gene_set.tests.factory import GeneSetFactory

from ..models import MethylResult


class MethylsFactory(GeneSetFactory):
    """Factory for Analysis Result's Microbe Directory."""

    class Meta:
        """Factory metadata."""

        model = MethylResult
