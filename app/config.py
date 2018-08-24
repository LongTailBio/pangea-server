"""Environment configurations."""

# pylint: disable=too-few-public-methods,invalid-name

import os


BASE_CELERY = {
    'broker_url': os.environ.get('CELERY_BROKER_URL'),
    'result_backend': os.environ.get('CELERY_RESULT_BACKEND'),
    'result_expires': 3600,     # Expire results after one hour
    'result_cache_max': None,   # Do not limit cache
    'task_always_eager': False,
    'task_eager_propagates': False,
    'task_serializer': 'json',
}


class Config(object):
    """Parent configuration class."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')
    BCRYPT_LOG_ROUNDS = 13
    TOKEN_EXPIRATION_DAYS = 30
    TOKEN_EXPIRATION_SECONDS = 0
    MAX_CONTENT_LENGTH = 100 * 1000 * 1000

    # Prevent MongoClient from connecting before Celery workers fork
    # http://api.mongodb.com/python/current/faq.html#is-pymongo-fork-safe
    MONGODB_CONNECT = False

    # Flask-API renderer
    DEFAULT_RENDERERS = [
        'app.api.renderers.EnvelopeJSONRenderer',
        'flask_api.renderers.BrowsableAPIRenderer',
    ]

    # Celery settings
    CELERY_CONFIG = BASE_CELERY


class DevelopmentConfig(Config):
    """Configurations for Development."""

    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    MONGODB_HOST = os.environ.get('MONGODB_TEST_HOST')
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRATION_DAYS = 0
    TOKEN_EXPIRATION_SECONDS = 3

    # Celery settings
    CELERY_CONFIG = dict(list(BASE_CELERY.items()) + list({
        'broker_url': os.environ.get('CELERY_BROKER_TEST_URL'),
        'result_backend': os.environ.get('CELERY_RESULT_TEST_BACKEND'),
        'task_always_eager': True,
        'task_eager_propagates': True,
    }.items()))


class StagingConfig(Config):
    """Configurations for Staging."""

    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""

    # Set these explicitly just to be extra safe
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MONGODB_HOST = os.environ.get('MONGODB_HOST')

    # Celery settings
    CELERY_CONFIG = dict(list(BASE_CELERY.items()) + list({
        'broker_url': os.environ.get('CELERY_BROKER_URL'),
        'result_backend': os.environ.get('CELERY_RESULT_BACKEND'),
    }.items()))


# pylint: disable=invalid-name
app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}
