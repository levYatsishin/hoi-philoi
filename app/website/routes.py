from flask import render_template, abort
from flask_login import login_required, current_user

from db_api import DBApi

from . import web_app

__all__ = []


@web_app.route('/')
@login_required
def index():
    return render_template('index.html', posts=[], username=current_user.get_data()['username'])


@web_app.route('/person/<username>')
@login_required
def personal(username):
    api = DBApi()
    person = api.get_user_by(username=username)

    if person is None:
        return abort(404)

    posts = api.get_posts_by(u_id_user=person['u_id_user'])
    posts = posts if posts is not None else []

    return render_template('personal.html', person=person, posts=posts)
