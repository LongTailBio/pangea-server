# pylint:disable=unused-import

"""Import celery from app module here to avoid cyclic dependency."""

from app import create_app

# Re-export
from app.extensions import celery


# Create app, thus configuring the celery instance in app.extensions
app = create_app()
