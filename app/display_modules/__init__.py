"""Modules for converting analysis tool output to front-end display data."""

from app.display_modules.ags import AGSDisplayModule
from app.display_modules.alpha_div import AlphaDivDisplayModule
from app.display_modules.beta_div import BetaDiversityDisplayModule
from app.display_modules.card_amrs import CARDGenesDisplayModule
from app.display_modules.functional_genes import FunctionalGenesDisplayModule
from app.display_modules.hmp import HMPDisplayModule
from app.display_modules.macrobes import MacrobeDisplayModule
from app.display_modules.methyls import MethylsDisplayModule
from app.display_modules.microbe_directory import MicrobeDirectoryDisplayModule
from app.display_modules.read_stats import ReadStatsDisplayModule
from app.display_modules.pathways import PathwaysDisplayModule
from app.display_modules.reads_classified import ReadsClassifiedModule
from app.display_modules.sample_similarity import SampleSimilarityDisplayModule
from app.display_modules.taxa_tree import TaxaTreeDisplayModule
from app.display_modules.taxon_abundance import TaxonAbundanceDisplayModule
from app.display_modules.virulence_factors import VirulenceFactorsDisplayModule


all_display_modules = [  # pylint: disable=invalid-name
    AGSDisplayModule,
    AlphaDivDisplayModule,
    BetaDiversityDisplayModule,
    CARDGenesDisplayModule,
    FunctionalGenesDisplayModule,
    HMPDisplayModule,
    MacrobeDisplayModule,
    MethylsDisplayModule,
    MicrobeDirectoryDisplayModule,
    PathwaysDisplayModule,
    ReadStatsDisplayModule,
    ReadsClassifiedModule,
    SampleSimilarityDisplayModule,
    TaxaTreeDisplayModule,
    TaxonAbundanceDisplayModule,
    VirulenceFactorsDisplayModule,
]
