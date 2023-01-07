from datetime import date

from flask import request, redirect, render_template
from flask_login import current_user

from db_api import PostgresApi
from . import pub_app
from .forms import Event, Post

__all__ = []


@pub_app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = Event()

    successful = False

    if request.method == 'POST':
        api = PostgresApi()

        successful = api.create_event(
            {'u_id_user': current_user.get_data()['u_id'], 'content': form.content.data,
             'publication_date': date.today(), 'time_start': form.time_start.data, 'time_end': form.time_end.data,
             'location': form.locate.data})

        if successful:
            return redirect('/')

    return render_template('make_event.html', form=form, successful=successful)


@pub_app.route('/create_postt', methods=['GET', 'POST'])
def create_post():
    form = Post()

    successful = False

    if request.method == 'POST':
        api = PostgresApi()

        successful = api.create_post(
            {'u_id_user': current_user.get_data()['u_id'], 'content': form.content.data,
             'publication_date': date.today()})

        if successful:
            return redirect('/')

    return render_template('make_postt.html', form=form, successful=successful)
