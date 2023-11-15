import json
from getpass import getpass
from os.path import basename, dirname, exists, isabs, join
import os
import sys
import webbrowser

import flask
import numpy as np
import yaml
from dotenv import load_dotenv, find_dotenv

from iris.extensions import db, compress
from iris.project import project


load_dotenv(find_dotenv())
project_file = os.environ.get("PROJECT_FILE")


def create_app(project_file):
    project.load_from(project_file)
    project.debug = os.environ.get('DEBUG', False)
    # Create the flask app:
    app = flask.Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + join(project['path'], 'iris.db')
    # Register the extensions:
    db.init_app(app)
    compress.init_app(app)
    return app


def register_extensions(app):
    from iris.main import main_app
    app.register_blueprint(main_app)
    from iris.segmentation import segmentation_app
    app.register_blueprint(segmentation_app, url_prefix="/segmentation")
    from iris.admin import admin_app
    app.register_blueprint(admin_app, url_prefix="/admin")
    from iris.help import help_app
    app.register_blueprint(help_app, url_prefix="/help")
    from iris.user import user_app
    app.register_blueprint(user_app, url_prefix="/user")


app = create_app(project_file)
from iris.models import User, Action

with app.app_context():
    db.create_all()
    db.session.commit()

register_extensions(app)


if __name__ == '__main__':
    app.run(debug=project.debug, host=project['host'], port=project['port'])
