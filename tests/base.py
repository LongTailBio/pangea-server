"""Defines base test suite to use for MetaGenScope tests."""

import logging

from flask_testing import TestCase

from app import create_app, db, celery, update_celery_settings
from app.config import app_config
from app.mongo import drop_mongo_collections


app = create_app()


class BaseTestCase(TestCase):
    """Base MetaGenScope test suite."""

    def create_app(self):
        """Create app configured for testing."""
        config_cls = app_config['testing']
        app.config.from_object(config_cls)
        update_celery_settings(celery, config_cls)
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

        # Mongo
        drop_mongo_collections()

        # Enable logging
        logging.disable(logging.NOTSET)
