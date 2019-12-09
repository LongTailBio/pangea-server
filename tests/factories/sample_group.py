# pylint: disable=too-few-public-methods

"""Factory for generating Sample Group models for testing."""

import factory

from app import db
from app.db_models import SampleGroup


class SampleGroupFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for Sample Group."""

    class Meta:
        """Factory metadata."""

        model = SampleGroup
        session = db.session

    name = factory.Faker('city')
    access_scheme = 'public'
