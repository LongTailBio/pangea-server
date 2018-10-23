"""Tasks for the Conductor module."""

from celery import Task

from app.extensions import celery_logger


class PluginTask(Task):  # pylint: disable=abstract-method
    """Base task for running plugin processors."""

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log error details."""
        celery_logger.warn('Arguments: %s', args)
