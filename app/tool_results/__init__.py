"""Modules for genomic analysis tool outputs."""

from .alpha_diversity import AlphaDiversityResultModule
from .ancestry import AncestryResultModule
from .beta_diversity import BetaDiversityResultModule
from .card_amrs import CARDAMRResultModule
from .food_pet import FoodPetResultModule
from .hmp_sites import HmpSitesResultModule
from .humann2 import Humann2ResultModule
from .humann2_normalize import Humann2NormalizeResultModule
from .kraken import KrakenResultModule
from .krakenhll import KrakenHLLResultModule
from .macrobes import MacrobeResultModule
from .metaphlan2 import Metaphlan2ResultModule
from .methyltransferases import MethylResultModule
from .microbe_census import MicrobeCensusResultModule
from .microbe_directory import MicrobeDirectoryResultModule
from .read_stats import ReadStatsToolResultModule
from .reads_classified import ReadsClassifiedResultModule
from .shortbred import ShortbredResultModule
from .vfdb import VFDBResultModule


all_tool_results = [  # pylint: disable=invalid-name
    AlphaDiversityResultModule,
    AncestryResultModule,
    BetaDiversityResultModule,
    CARDAMRResultModule,
    FoodPetResultModule,
    HmpSitesResultModule,
    Humann2ResultModule,
    Humann2NormalizeResultModule,
    KrakenResultModule,
    KrakenHLLResultModule,
    MacrobeResultModule,
    Metaphlan2ResultModule,
    MethylResultModule,
    MicrobeCensusResultModule,
    MicrobeDirectoryResultModule,
    ReadStatsToolResultModule,
    ReadsClassifiedResultModule,
    ShortbredResultModule,
    VFDBResultModule,
]
