"""Test suites for application configurations."""

import os
import unittest

from flask import current_app
from flask_testing import TestCase

from app import create_app
from app.config import app_config


app = create_app()


class TestDevelopmentConfig(TestCase):
    """Test suite for development configuration."""

    def create_app(self):
        app.config.from_object(app_config['development'])
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


class TestTestingConfig(TestCase):
    """Test suite for testing configuration."""

    def create_app(self):
        app.config.from_object(app_config['testing'])
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


class TestProductionConfig(TestCase):
    """Test suite for production configuration."""

    def create_app(self):
        app.config.from_object(app_config['production'])
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


if __name__ == '__main__':
    unittest.main()
