from flask import render_template
from flask_login import login_required, current_user

from db_api import DBApi

from . import web_app

__all__ = []


@web_app.route('/')
@login_required
def index():
    print(current_user.get_data())
    return render_template('index.html', posts=[])


@web_app.route('/person/<username>')
def personal(username):
    api = DBApi()
    user = api.get_user_by(username=username)
    posts = api.get_posts_by(u_id_user='posts')

    return render_template('personal.html', person=user, posts=posts)
