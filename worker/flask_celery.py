"""Flask adapter for Celery."""

from collections import namedtuple

from celery import Celery as BaseCelery
from flask import Flask


class Celery(BaseCelery):
    """Main class used for initialization of Flask-Celery."""

    def __init__(self, *args, app=None, config=None, **kwargs):
        """Initialize Celery."""
        self.app = None

        super(Celery, self).__init__(*args, **kwargs)

        if app is not None:
            self.init_app(app, config)

    def init_app(self, app, config=None):
        """Initialize with Flask app."""
        if not app or not isinstance(app, Flask):
            raise Exception('Invalid Flask application instance')

        self.app = app

        app.extensions = getattr(app, 'extensions', {})

        if 'celery' not in app.extensions:
            app.extensions['celery'] = {}

        if self in app.extensions['celery']:
            # Raise an exception if extension already initialized as
            # potentially new configuration would not be loaded.
            raise Exception('Extension already initialized')

        if not config:
            # If not passed a config then we read the connection settings
            # from the app config.
            self.update_from_app(app)

        # Store objects in application instance so that multiple apps do not
        # end up accessing the same objects.
        store = {'app': app}
        app.extensions['celery'][self] = store

    def update_from_app(self, app):
        """Update Celery configuration from Flask app."""
        celery_conf = app.config['CELERY_CONFIG']
        # Convert dict to object in order for config_from_object to accept it
        celery_conf = namedtuple('CeleryConf', celery_conf.keys())(*celery_conf.values())
        self.config_from_object(celery_conf)
