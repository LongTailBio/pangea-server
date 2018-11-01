# pylint: disable=missing-docstring,too-few-public-methods

"""Factory for generating Microbe Directory models for testing."""

from analysis_packages.generic_gene_set.tests.factory import GeneSetFactory

from ..models import CARDGenesResult


class CARDGenesFactory(GeneSetFactory):
    """Factory for CARD Genes."""

    class Meta:
        """Factory metadata."""

        model = CARDGenesResult
