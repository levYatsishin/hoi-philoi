from flask import render_template

from . import pub_app


@pub_app.route('/create_post')
def make_event():

    return render_template('make_event.html')
