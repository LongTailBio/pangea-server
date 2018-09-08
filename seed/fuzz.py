"""Create and save a Sample Group with all the fixings (plus gravy)."""

from uuid import uuid4

from analysis_packages.ags.tests.factory import AGSFactory
from analysis_packages.card_amrs.tests.factory import CARDGenesFactory
from analysis_packages.functional_genes.tests.factory import FunctionalGenesFactory
from analysis_packages.hmp.tests.factory import HMPFactory
from analysis_packages.macrobes.tests.factory import MacrobeFactory
from analysis_packages.methyls.tests.factory import MethylsFactory
from analysis_packages.microbe_directory.tests.factory import MicrobeDirectoryFactory
from analysis_packages.multi_axis.tests.factory import MultiAxisFactory
from analysis_packages.pathways.tests.factory import PathwayFactory
from analysis_packages.read_stats.tests.factory import ReadStatsFactory
from analysis_packages.reads_classified.tests.factory import ReadsClassifiedFactory
from analysis_packages.sample_similarity.tests.factory import SampleSimilarityFactory
from analysis_packages.top_taxa.tests.factory import TopTaxaFactory
from analysis_packages.virulence_factors.tests.factory import VFDBFactory

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.sample_groups.sample_group_models import SampleGroup


def wrap_result(result):
    """Wrap display result in status wrapper."""
    return AnalysisResultWrapper(status='S', data=result).save()


def create_saved_group(uuid=None):
    """Create and save a Sample Group with all the fixings (plus gravy)."""
    if uuid is None:
        uuid = uuid4()
    analysis_result = AnalysisResultMeta().save()
    group_description = 'Includes factory-produced analysis results from all display_modules'
    sample_group = SampleGroup(name='Fuzz Testing',
                               analysis_result=analysis_result,
                               description=group_description)
    sample_group.id = uuid
    db.session.add(sample_group)
    db.session.commit()

    # Add the results
    analysis_result.average_genome_size = wrap_result(AGSFactory())
    analysis_result.card_amr_genes = wrap_result(CARDGenesFactory())
    analysis_result.functional_genes = wrap_result(FunctionalGenesFactory())
    analysis_result.hmp = wrap_result(HMPFactory())
    analysis_result.macrobe_abundance = wrap_result(MacrobeFactory())
    analysis_result.methyltransferases = wrap_result(MethylsFactory())
    analysis_result.microbe_directory = wrap_result(MicrobeDirectoryFactory())
    analysis_result.multi_axis_abundance = wrap_result(MultiAxisFactory())
    analysis_result.pathways = wrap_result(PathwayFactory())
    analysis_result.read_stats = wrap_result(ReadStatsFactory())
    analysis_result.reads_classified = wrap_result(ReadsClassifiedFactory())
    analysis_result.sample_similarity = wrap_result(SampleSimilarityFactory())
    # analysis_result.taxon_abundance =
    analysis_result.top_taxa = wrap_result(TopTaxaFactory())
    analysis_result.virulence_factors = wrap_result(VFDBFactory())
    analysis_result.save()

    return sample_group
