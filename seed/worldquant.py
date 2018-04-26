"""Create and save a Sample Group with everything for WorldQuant demo site."""

from uuid import UUID, uuid4

from app import db
from app.analysis_results.analysis_result_models import AnalysisResultMeta, AnalysisResultWrapper
from app.display_modules.alpha_div.tests.factory import AlphaDivFactory
from app.display_modules.beta_div.tests.factory import BetaDiversityFactory
from app.display_modules.card_amrs.tests.factory import CARDGenesFactory
from app.display_modules.functional_genes.tests.factory import FunctionalGenesFactory
from app.display_modules.macrobes.tests.factory import MacrobeFactory
from app.display_modules.methyls.tests.factory import MethylsFactory
from app.display_modules.microbe_directory.tests.factory import MicrobeDirectoryFactory
from app.display_modules.pathways.tests.factory import PathwayFactory
from app.display_modules.read_stats.tests.factory import ReadStatsFactory
from app.display_modules.reads_classified.tests.factory import ReadsClassifiedFactory
from app.display_modules.taxa_tree.tests.factory import TaxaTreeFactory
from app.display_modules.virulence_factors.tests.factory import VFDBFactory
from app.display_modules.volcano.tests.factory import VolcanoFactory

from app.samples.sample_models import Sample
from app.sample_groups.sample_group_models import SampleGroup

from .abrf_2017 import sample_similarity, taxon_abundance, hmp, ags
from .uw_madison import load_reads_classified


def wrap_result(result):
    """Wrap display result in status wrapper."""
    return AnalysisResultWrapper(status='S', data=result)


def create_saved_sample(index, uuid=None):
    """Create and save a Sample with all the fixings (plus gravy)."""
    print(f'Creating sample #{index}')

    if uuid is None:
        uuid = UUID(f'00000000-0000-4000-8000-100000000{index:03}')

    analysis_result = AnalysisResultMeta()

    # Add results
    analysis_result.reads_classified = wrap_result(load_reads_classified())
    analysis_result.taxa_tree = wrap_result(TaxaTreeFactory())
    analysis_result.card_amr_genes = wrap_result(CARDGenesFactory())
    analysis_result.methyltransferases = wrap_result(MethylsFactory())
    analysis_result.virulence_factors = wrap_result(VFDBFactory())
    analysis_result.functional_genes = wrap_result(FunctionalGenesFactory())

    # Persist analysis result
    analysis_result.save()

    sample = Sample(uuid=uuid,
                    name=f'SomethingUnique_{index}',
                    theme='world-quant-sample',
                    analysis_result=analysis_result).save()

    return sample


def create_saved_group(uuid=None):
    """Create and save a Sample Group with all the fixings (plus gravy)."""
    if uuid is None:
        uuid = uuid4()
    analysis_result = AnalysisResultMeta().save()
    group_description = 'April 29 - May 2, 2018: Los Angeles'
    sample_group = SampleGroup(name='2018 Milken Conference',
                               analysis_result=analysis_result,
                               description=group_description,
                               theme='world-quant')
    sample_group.id = uuid
    sample_group.samples = [create_saved_sample(i) for i in range(100)]
    db.session.add(sample_group)
    db.session.commit()

    # Add the results
    analysis_result.alpha_diversity = wrap_result(AlphaDivFactory())
    analysis_result.average_genome_size = ags
    analysis_result.beta_diversity = wrap_result(BetaDiversityFactory())
    analysis_result.card_amr_genes = wrap_result(CARDGenesFactory())
    analysis_result.functional_genes = wrap_result(FunctionalGenesFactory())
    analysis_result.hmp = hmp
    analysis_result.macrobe_abundance = wrap_result(MacrobeFactory())
    analysis_result.methyltransferases = wrap_result(MethylsFactory())
    analysis_result.microbe_directory = wrap_result(MicrobeDirectoryFactory())
    analysis_result.pathways = wrap_result(PathwayFactory())
    analysis_result.read_stats = wrap_result(ReadStatsFactory())
    analysis_result.reads_classified = wrap_result(ReadsClassifiedFactory())
    analysis_result.sample_similarity = sample_similarity
    analysis_result.taxon_abundance = taxon_abundance
    analysis_result.virulence_factors = wrap_result(VFDBFactory())
    analysis_result.volcano = wrap_result(VolcanoFactory())
    analysis_result.save()

    return sample_group
