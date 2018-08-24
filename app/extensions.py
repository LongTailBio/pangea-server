# pylint: disable=invalid-name

"""App extensions defined here to avoid cyclic imports."""

from multiprocessing import Lock

from celery.utils.log import get_task_logger

from flask_mongoengine import MongoEngine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from worker.flask_celery import Celery


sample_upload_lock = Lock()
persist_result_lock = Lock()
mongoDB = MongoEngine()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

# Celery w/ Flask facory pattern from:
#   https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern
celery = Celery(main=__name__)
celery_logger = get_task_logger(__name__)
