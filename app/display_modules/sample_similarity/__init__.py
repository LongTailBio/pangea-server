"""
Sample Similarity module.

This plot displays a dimensionality reduction of the data.

Samples are drawn near to similar samples in high dimensional space using a
machine learning algorithm: T-Stochastic Neighbours Embedding.

The plot can be colored by different sample metadata and the position of the
points can be adjust to reflect the analyses of different tools.
"""

from app.display_modules.display_module import DisplayModule

# Re-export modules
from app.display_modules.sample_similarity.sample_similarity_models import (
    SampleSimilarityResult,
    ToolDocument,
)


class SampleSimilarityDisplayModule(DisplayModule):
    """Sample Similarity display module."""

    @classmethod
    def name(cls):
        """Return module's unique identifier string."""
        return 'sample_similarity'

    @classmethod
    def get_result_model(cls):
        """Return data model for Sample Similarity type."""
        return SampleSimilarityResult
