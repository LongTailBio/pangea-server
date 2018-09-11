"""MetaGenScope server application."""

import os

from flask import jsonify, current_app, Blueprint
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from app.analysis_modules import all_analysis_modules
from app.analysis_modules.register import register_display_module
from app.api.constants import URL_PREFIX
from app.api.v1.analysis_results import analysis_results_blueprint
from app.api.v1.auth import auth_blueprint
from app.api.v1.organizations import organizations_blueprint
from app.api.v1.ping import ping_blueprint
from app.api.v1.samples import samples_blueprint
from app.api.v1.sample_groups import sample_groups_blueprint
from app.api.v1.users import users_blueprint
from app.config import app_config
from app.extensions import mongoDB, db, migrate, bcrypt, celery
from app.tool_results import all_tool_results
from app.tool_results.register import register_tool_result


def create_app(environment=None):
    """Create and bootstrap app."""
    # Instantiate the app
    app = FlaskAPI(__name__)

    # Enable CORS
    CORS(app)

    # Set config
    if not environment:
        environment = os.getenv('APP_SETTINGS', 'development')
    config_object = app_config[environment]
    app.config.from_object(config_object)

    # Set up extensions
    mongoDB.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)

    # Register application components
    register_tool_result_modules(app)
    register_display_modules(app)
    register_blueprints(app)
    register_error_handlers(app)

    return app


def register_tool_result_modules(app):
    """Register each Tool Result module."""
    tool_result_modules_blueprint = Blueprint('tool_result_modules', __name__)
    for tool_result in all_tool_results:
        register_tool_result(tool_result, tool_result_modules_blueprint)
    app.register_blueprint(tool_result_modules_blueprint, url_prefix=URL_PREFIX)


def register_display_modules(app):
    """Register each Display Module."""
    display_modules_blueprint = Blueprint('display_modules', __name__)
    for module in all_analysis_modules:
        register_display_module(module, display_modules_blueprint)
    app.register_blueprint(display_modules_blueprint, url_prefix=URL_PREFIX)


def register_blueprints(app):
    """Register API endpoint blueprints for app."""
    app.register_blueprint(analysis_results_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(auth_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(organizations_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(ping_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(samples_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(sample_groups_blueprint, url_prefix=URL_PREFIX)
    app.register_blueprint(users_blueprint, url_prefix=URL_PREFIX)


def register_error_handlers(app):
    """Register JSON error handlers for app."""
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_error)


def page_not_found(not_found_error):
    """Handle 404 Not Found error."""
    return jsonify(error=404, text=str(not_found_error)), 404


def internal_error(exception):
    """Handle 500 Internal Error error."""
    current_app.logger.exception(exception)
    return jsonify(error=500, text=str(exception)), 500
