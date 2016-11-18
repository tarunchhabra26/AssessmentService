__author__ = "Tarun Chhabra"

__version__ = 1.0
version = __version__

import os

from flask import Flask,render_template
from flask.ext.sqlalchemy import SQLAlchemy
from logbook import Logger

from restapi import config
from utils.logging import LoggingSetup, ProductionLoggingSetup

# Start flask
app = Flask(__name__)
config_name = os.getenv('ASSESSMENTAPICONFIG', 'DefaultConfig')

# Configurations
API_CONFIG = config.defined[config_name]
app.config.from_object(API_CONFIG)

# Setup SQLAlchemy
db = SQLAlchemy(app)

# Logging
log = Logger(__name__)
log_setup = ProductionLoggingSetup(app.config['LOG_LEVEL'], app.config['LOG_DIR'] + '%s.log' % app.config['APP_NAME'])
log_to_file = log_setup.get_default_setup()

# Load App Key Auth Decorators
from restapi.components.auth.decorators import require_app_key

## API routing
from modules.organization import mod as organizations_module
app.register_blueprint(organizations_module)

from modules.assignment import mod as assignment_module
app.register_blueprint(assignment_module)

from modules.student import mod as student_module
app.register_blueprint(student_module)

from modules.score import  mod as score_module
app.register_blueprint(score_module)

"""
Routes that does not matter.
"""


@app.route('/', methods=['GET', 'OPTIONS'])
def api_root():
    """
    Just a route that says hello to the client if he goes to the root of the API. You can remove this if you want.
    """
    body = "Hi, this is a RESTful API." \
           "\n Before using it you should be issued a API key from your friendly developer.."
    return render_template('front.html', content=body, title="Awesome API", version=version)


@app.route("/version", methods=['GET', 'OPTIONS'])
@require_app_key
def api_latest_version():
    """
    Check version of the API, protected with authorization.
    """
    return str(version)