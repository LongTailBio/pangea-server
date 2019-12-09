"""Defines base test suite to use for MetaGenScope tests."""

import logging
import psycopg2

from flask_testing import TestCase
from testing.postgresql import PostgresqlFactory

from app import create_app, db
from app.config import app_config


app = create_app()


def db_init_handler(postgresql):
    conn = psycopg2.connect(**postgresql.dsn())
    cursor = conn.cursor()
    cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
    cursor.close()
    conn.commit()
    conn.close()


Postgresql = PostgresqlFactory(
    cache_initialized_db=True, on_initialized=db_init_handler
)


class BaseTestCase(TestCase):
    """Base MetaGenScope test suite."""

    def create_app(self):
        """Create app configured for testing."""
        config_cls = app_config['testing']
        app.config.from_object(config_cls)
        return app

    def setUp(self):
        """Set up test DB."""
        self.postgresql = Postgresql()
        app.config['SQLALCHEMY_DATABASE_URI'] = self.postgresql.url()
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
        self.postgresql.stop()
