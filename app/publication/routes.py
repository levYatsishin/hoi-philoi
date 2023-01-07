from flask import render_template

from . import pub_app

__all__ = []


@pub_app.route('/create_event')
def create_event():
    return render_template('make_event.html')
