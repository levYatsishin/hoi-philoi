from flask import Blueprint

auth_app = Blueprint('auth_app', __name__)

from . import routes
