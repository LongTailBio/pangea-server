"""Flask adapter for Celery."""

from collections import namedtuple

from celery import Celery
import flask


class FlaskCelery(Celery):
    """Main class used for initialization of Flask-Celery."""

    def __init__(self, *args, **kwargs):
        """Initialize FlaskCelery instance."""
        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def patch_task(self):
        """Patch base task to use application context."""
        TaskBase = self.Task  # pylint: disable=invalid-name
        _celery = self

        class ContextTask(TaskBase):  # pylint: disable=too-few-public-methods
            """Celery Task that runs within application context."""

            abstract = True

            def __call__(self, *args, **kwargs):
                if flask.has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask  # pylint: disable=invalid-name

    def init_app(self, app):
        """Initialize Celery instance from Flask app."""
        self.app = app
        self.update_from_app(app)

    def update_from_app(self, app):
        """Update Celery configuration from Flask app."""
        celery_conf = app.config['CELERY_CONFIG']
        # Convert dict to object in order for config_from_object to accept it
        celery_conf = namedtuple('CeleryConf', celery_conf.keys())(*celery_conf.values())
        self.config_from_object(celery_conf)
