"""
This is main module for app factory, it contains function
for configure app, initializes extension.
"""

import os
from flask import Flask, render_template
from app.extensions import DB, API
from config import Config

__all__ = ['create_app']


def create_app(config_file=None):
    """This factory function create app object with parameters send toi function."""

    app = Flask(__name__)

    configure_app(app, config_file)
    configure_extensions(app)

    blueprints = app.config['BLUEPRINTS']

    configure_blueprints(app, blueprints)

    return app


def configure_app(app, config_file=None):
    """
    This function configure app. Default config is from Config class.
    If you need, you can pass config file by parameter.
    """

    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(Config)

    # example file is config.cfg
    # http://flask.pocoo.org/docs/config/#instance-folders
    if config_file:
        additional_config = os.path.join(os.path.dirname(app.instance_path), config_file)
        app.config.from_pyfile(additional_config, silent=True)


def configure_extensions(app):
    """
    This function configures all extensions used in app.
    """

    DB.init_app(app)

    with app.app_context():
        DB.create_all()
        DB.session.commit()


def configure_blueprints(app, blueprints):
    """
    This function configures blueprints which are passed to function.
    """

    for blueprint_config in blueprints:
        name, rest = None, {}

    if isinstance(blueprint_config, basestring):
        name = blueprint_config
    elif isinstance(blueprint_config, (list, tuple)):
        name = blueprint_config[0]
        rest.update(blueprint_config[1])
    else:
        raise Exception('Bad blueprint config.')

    add_blueprint(app, name, rest)


def add_blueprint(app, name, rest):
    """This function register blueprint in application app."""
    blueprint = import_variable(name, 'views', 'BLUEPRINT')
    app.register_blueprint(blueprint, **rest)


def import_variable(blueprint_path, module, variable_name):
    """This function import package and returns bluepritn to register."""
    path = '.'.join(['app'] + blueprint_path.split('.') + [module])
    mod = __import__(path, fromlist=[variable_name])
    return getattr(mod, variable_name)


def configure_error_handlers(app):
    """Configure error handlers."""

    @app.errorhandler(403)
    def forbidden(error):
        """Forbidden page"""
        return render_template('403.html', error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        """Not Found page"""
        return render_template('404.html', error=error), 404

    @app.errorhandler(500)
    def server_error(error):
        """Server error"""
        return render_template('500.html', error=error), 500