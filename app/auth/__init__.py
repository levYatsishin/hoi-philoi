from flask import Blueprint

from . import forms

auth_app = Blueprint('auth_app', __name__)

from . import routes
