from flask import Blueprint

web_app = Blueprint('web_app', __name__)

from . import routes
