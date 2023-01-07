from flask import render_template, redirect, abort
from flask_login import login_required, current_user

from db_api import DBApi

from . import web_app

__all__ = []


@web_app.route('/')
@login_required
def index():
    api = DBApi()

    events = api.get_events_by(u_id_user=current_user.get_data()['u_id_user'])

    return render_template('index.html', events=events)


@web_app.route('/person/')
@web_app.route('/person/<username>')
@login_required
def personal(username=''):
    if username == '':
        return redirect(f"/person/{current_user.get_data()['username']}")

    api = DBApi()
    person = api.get_user_by(username=username)

    if person is None:
        return abort(404)

    posts = api.get_posts_by(u_id_user=person['u_id_user'])
    posts = posts if posts is not None else []

    return render_template('personal.html', person=person, posts=posts, user_subscribed=False)


@web_app.route('/person/<username>/subscribers')
@login_required
def subscribers(username):
    api = DBApi()
    person = api.get_user_by(username=username)

    if person is None:
        return abort(404)

    subscribers_ids = api.get_subscribers_by(u_id_user=person['u_id_user'])

    user_subscribers = []

    if subscribers_ids is not None:
        for user_id in subscribers_ids:
            user_subscribers.append(api.get_user_by(u_id_user=user_id))

    return render_template('subscribers.html', person=person, subscribers=user_subscribers)


@web_app.route('/person/<username>/subscribe')
@login_required
def subscribe(username):
    api = DBApi()

    user = api.get_user_by(username=username)
    if user is None:
        return abort(404)

    api.change_subscription_state(user['u_id_user'], current_user.get_id())

    return redirect(f'/person/{username}')
