import os

import flask
from dotenv import load_dotenv, find_dotenv

from iris.project import project


load_dotenv(find_dotenv())
project_file = os.environ.get("PROJECT_FILE")

def create_app(project_file):
    project.load_from(project_file)
    # Create the flask app:
    app = flask.Flask(__name__)
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'sqlite:///' + os.path.join(project['path'], 'iris.db')
    return app

app = create_app(project_file=project_file)

