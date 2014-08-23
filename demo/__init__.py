#!/usr/bin/env python

'''The demo module, containing the app factory function.'''
from flask import Flask

from demo.settings import ProdConfig
from demo.extensions import (
    db,
    migrate,
)
from demo.api import api_blueprint


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)


def register_blueprints(app):
    app.register_blueprint(api_blueprint)
