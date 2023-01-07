from flask import Blueprint

from . import routes

pub_app = Blueprint('pub_app', __name__)

from . import routes
