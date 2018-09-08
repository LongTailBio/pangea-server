"""Handle loading data from JSON files."""

import json
import os

from analysis_packages.reads_classified.models import ReadsClassifiedResult


LOCATION = os.path.realpath(os.path.join(os.getcwd(),
                                         os.path.dirname(__file__)))


def load_reads_classified():
    """Load Reads Classified source JSON."""
    filename = os.path.join(LOCATION, 'reads-classified.json')
    with open(filename, 'r') as source:
        samples = {'UW_Madison_00': json.load(source)}
        result = ReadsClassifiedResult(samples=samples)
        return result
