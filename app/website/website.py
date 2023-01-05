from flask import render_template
from flask_login import login_required

from . import web_app

__all__ = []


@web_app.route('/')
@login_required
def index():
    return render_template('index.html')
