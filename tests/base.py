"""Defines base test suite to use for MetaGenScope tests."""

import logging

from flask_testing import TestCase

from app import create_app, db, celery
from app.config import app_config


app = create_app()


class BaseTestCase(TestCase):
    """Base MetaGenScope test suite."""

    def create_app(self):
        """Create app configured for testing."""
        config_cls = app_config['testing']
        app.config.from_object(config_cls)
        celery.update_from_app(app)
        return app

    def setUp(self):
        """Set up test DB."""
        db.create_all()
        db.session.commit()

        # Disable logging
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        """Tear down test DBs."""
        # Postgres
        db.session.remove()
        db.drop_all()

        # Enable logging
        logging.disable(logging.NOTSET)
