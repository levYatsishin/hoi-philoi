from flask import redirect, request, render_template
from flask_login import login_user, logout_user

from werkzeug.security import generate_password_hash, check_password_hash

from .forms import LoginForm, RegisterForm
from . import auth_app

from units import User
from db_api import DBApi

__all__ = []


@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        user = DBApi().get_user_by(username=form.login.data)

        if check_password_hash(user['password_hash'], form.password.data):
            login_user(User(user['u_id_user']))

            return redirect('/')

    return render_template('login.html', form=form)


@auth_app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        success = DBApi().create_user({'name': form.name, 'username': form.username, 'mail': form.mail,
                                       'password_hash': generate_password_hash(form.password.data)})
        if success:
            return redirect('/login')

    return render_template('register.html', form=form)


@auth_app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
