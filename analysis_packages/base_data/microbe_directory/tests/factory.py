"""Factory for generating Kraken result models for testing."""

from random import random

from .. import MicrobeDirectoryToolResult


def create_values():
    """Create microbe directory values."""
    return {
        'gram_stain': {
            'gram_positive': random(),
            'gram_negative': random(),
            'unknown': random(),
        },
        'microbiome_location': {
            'human': random(),
            'non_human': random(),
            'unknown': random(),
        },
        'antimicrobial_susceptibility': {
            'known_abx': random(),
            'unknown': random(),
        },
        'optimal_temperature': {
            '37c': random(),
            'unknown': random(),
        },
        'extreme_environment': {
            'mesophile': random(),
            'unknown': random(),
        },
        'biofilm_forming': {
            'yes': random(),
            'unknown': random(),
        },
        'optimal_ph': {
            'unknown': random(),
        },
        'animal_pathogen': {
            'unknown': random(),
        },
        'spore_forming': {
            'no': random(),
            'unknown': random(),
        },
        'pathogenicity': {
            'cogem_1': random(),
            'cogem_2': random(),
            'unknown': random(),
        },
        'plant_pathogen': {
            'no': random(),
            'unknown': random(),
        }
    }


def create_result(save=True):
    """Create MicrobeDirectoryToolResult with randomized field data."""
    packed_data = create_values()
    result = MicrobeDirectoryToolResult(**packed_data)
    if save:
        result.save()
    return result
