# pylint: disable=too-few-public-methods disable=no-self-use

"""Factory for generating Kraken result models for testing."""

from random import random

import factory

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


class MicrobeDirectoryToolResultFactory(factory.mongoengine.MongoEngineFactory):
    """Factory for base ancestry data."""

    class Meta:
        """Factory metadata."""

        model = MicrobeDirectoryToolResult

        @factory.lazy_attribute
        def gram_stain(self):
            """Return microbe directory stuff."""
            return {
                'gram_positive': random(),
                'gram_negative': random(),
                'unknown': random(),
            }

        @factory.lazy_attribute
        def microbiome_location(self):
            """Return microbe directory stuff."""
            return {
                'human': random(),
                'non_human': random(),
                'unknown': random(),
            }

        @factory.lazy_attribute
        def antimicrobial_susceptibility(self):
            """Return microbe directory stuff."""
            return {
                'known_abx': random(),
                'unknown': random(),
            }

        @factory.lazy_attribute
        def optimal_temperature(self):
            """Return microbe directory stuff."""
            return {
                '37c': random(),
                'unknown': random(),
            }

        @factory.lazy_attribute
        def extreme_environment(self):
            """Return microbe directory stuff."""
            return {
                'mesophile': random(),
                'unknown': random(),
            }

        @factory.lazy_attribute
        def biofilm_forming(self):
            """Return microbe directory stuff."""
            return {
                'yes': random(),
                'unknown': random(),
            }

        @factory.lazy_attribute
        def optimal_ph(self):
            """Return microbe directory stuff."""
            return {
                'unknown': random(),
            }

        @factory.lazy_attribute
        def animal_pathogen(self):
            """Return microbe directory stuff."""
            return {
                'unknown': random(),
            }

        @factory.lazy_attribute
        def spore_forming(self):
            """Return microbe directory stuff."""
            return {
                'no': random(),
                'unknown': random(),
            }

        @factory.lazy_attribute
        def pathogenicity(self):
            """Return microbe directory stuff."""
            return {
                'cogem_1': random(),
                'cogem_2': random(),
                'unknown': random(),
            }

        @factory.lazy_attribute
        def plant_pathogen(self):
            """Return microbe directory stuff."""
            return {
                'no': random(),
                'unknown': random(),
            }
