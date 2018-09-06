"""
Asynchronous worker application for processing MetaGenScope queries.

Worker processes should run the celery instance in worker.worker which will be
configured to execute within the application context.

Celery w/ Flask facory pattern from:
  https://blog.miguelgrinberg.com/post/celery-and-the-flask-application-factory-pattern
"""
