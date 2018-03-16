"""Test suite for Sample Similarity tasks."""

from app.display_modules.sample_similarity.sample_similarity_tasks import (
    get_clean_samples,
    run_tsne,
    label_tsne,
    taxa_tool_tsne,
)
from app.samples.sample_models import Sample
from app.tool_results.kraken.tests.kraken_factory import create_kraken

from tests.base import BaseTestCase


class TestSampleSimilarityTasks(BaseTestCase):
    """Test suite for Sample Similarity tasks."""

    def test_clean_samples(self):
        """Ensure get_clean_samples method adds missing features to all samples."""
        sample_dict = {f'SMPL_{i}': create_kraken().taxa for i in range(3)}

        all_feature_ids = set([])
        for feature_set in sample_dict.values():
            all_feature_ids |= set(feature_set.keys())

        result = get_clean_samples(sample_dict, no_zero_features=False)

        for feature_set in result.values():
            for feature_id in all_feature_ids:
                self.assertIn(feature_id, feature_set)

    def test_clean_zeroed_samples(self):
        """Ensure get_clean_samples method removes features below threshold."""
        sample_dict = {f'SMPL_{i}': dict(create_kraken().taxa) for i in range(3)}
        sample_dict['SMPL_1']['somebadkingdom'] = 0.0000001

        all_feature_ids = set([])
        for feature_set in sample_dict.values():
            all_feature_ids |= set(feature_set.keys())

        result = get_clean_samples(sample_dict)

        for feature_set in result.values():
            self.assertNotIn('somebadkingdom', feature_set)

    def test_tsne_returns_data(self):
        """
        Ensure run_tsne method returns array of the correct size.

        tSNE is non-deterministic so that is as close as we can get to a real test.
        """
        sample_dict = {f'SMPL_{i}': dict(create_kraken().taxa) for i in range(3)}
        tsne_output = run_tsne(sample_dict)
        self.assertEqual((3, 2), tsne_output.shape)

    def test_label_tsne(self):
        """Ensure results are labeled correctly."""
        tsne_results = [[0, 1],
                        [2, 3],
                        [4, 5]]
        sample_names = ['SMPL_0', 'SMPL_1', 'SMPL_2']
        tool_label = 'kraken'
        labeled_samples = label_tsne(tsne_results, sample_names, tool_label)
        self.assertIn('kraken_x', labeled_samples['SMPL_0'])
        self.assertEqual(1, labeled_samples['SMPL_0']['kraken_y'])

    def test_taxa_tool_tsne_task(self):
        """Ensure taxa_tool_tsne task returns correct results."""
        samples = [Sample(name=f'SMPL_{i}', kraken=create_kraken()) for i in range(3)]
        tool, tsne_labeled = taxa_tool_tsne(samples, 'kraken')
        self.assertEqual('kraken tsne x', tool['x_label'])
        self.assertEqual('kraken tsne y', tool['y_label'])
        self.assertEqual(len(tsne_labeled), 3)
        self.assertIn('kraken_x', tsne_labeled['SMPL_0'])
        self.assertIn('kraken_y', tsne_labeled['SMPL_0'])
