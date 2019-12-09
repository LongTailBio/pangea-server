"""Environment configurations."""

import os


class Config():
    """Parent configuration class."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    MAX_CONTENT_LENGTH = 100 * 1000 * 1000

    # Flask-API renderer
    DEFAULT_RENDERERS = [
        'app.api.renderers.EnvelopeJSONRenderer',
        'flask_api.renderers.BrowsableAPIRenderer',
    ]

    # S3 Settings
    S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL', 'https://s3.wasabisys.com')
    S3_KEY_PREFIX = os.environ.get('S3_KEY_PREFIX', '')


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    DEBUG = True
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY', 'foo')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""

    # Set these explicitly just to be extra safe
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# pylint: disable=invalid-name
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
