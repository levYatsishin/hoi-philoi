from flask import Blueprint

from . import forms

pub_app = Blueprint('pub_app', __name__)

from . import routes
