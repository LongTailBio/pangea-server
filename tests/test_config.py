"""Test suites for application configurations."""

import os
import unittest

from flask import current_app
from flask_testing import TestCase

from app import create_app
from app.config import app_config
from app.extensions import celery


app = create_app()


class TestDevelopmentConfig(TestCase):
    """Test suite for development configuration."""

    def create_app(self):
        app.config.from_object(app_config['development'])
        celery.update_from_app(app)
        return app

    def test_app_is_development(self):
        """Ensure appropriate configuration values for development environment."""
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 30)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 0)
        self.assertTrue(
            app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_URL')
        )

        # Celery settings
        self.assertTrue(
            celery.conf.broker_url ==
            os.environ.get('CELERY_BROKER_URL')
        )
        self.assertTrue(
            celery.conf.result_backend ==
            os.environ.get('CELERY_RESULT_BACKEND')
        )


class TestTestingConfig(TestCase):
    """Test suite for testing configuration."""

    def create_app(self):
        app.config.from_object(app_config['testing'])
        celery.update_from_app(app)
        return app

    def test_app_is_testing(self):
        """Ensure appropriate configuration values for testing environment."""
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 4)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 0)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 3)
        self.assertTrue(
            app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )

        # Celery settings
        self.assertTrue(
            celery.conf.broker_url ==
            os.environ.get('CELERY_BROKER_TEST_URL')
        )
        self.assertTrue(
            celery.conf.result_backend ==
            os.environ.get('CELERY_RESULT_TEST_BACKEND')
        )


class TestProductionConfig(TestCase):
    """Test suite for production configuration."""

    def create_app(self):
        app.config.from_object(app_config['production'])
        celery.update_from_app(app)
        return app

    def test_app_is_production(self):
        """Ensure appropriate configuration values for production environment."""
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])
        self.assertTrue(app.config['BCRYPT_LOG_ROUNDS'] == 13)
        self.assertTrue(app.config['TOKEN_EXPIRATION_DAYS'] == 30)
        self.assertTrue(app.config['TOKEN_EXPIRATION_SECONDS'] == 0)
        self.assertTrue(
            app.config['SECRET_KEY'] ==
            os.environ.get('SECRET_KEY')
        )

        # Celery settings
        self.assertTrue(
            celery.conf.broker_url ==
            os.environ.get('CELERY_BROKER_URL')
        )
        self.assertTrue(
            celery.conf.result_backend ==
            os.environ.get('CELERY_RESULT_BACKEND')
        )


if __name__ == '__main__':
    unittest.main()
