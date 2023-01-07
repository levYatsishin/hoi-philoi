from flask import request, render_template
from flask_login import current_user

from db_api import PostgresApi
from forms import Event
from . import pub_app

__all__ = []


@pub_app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = Event()

    if request.method == 'POST':
        api = PostgresApi()

        api.create_event({'u_id_user': current_user.get_data()['u_id_user'], 'content': form.content.data})

    return render_template('make_event.html', form=form)
