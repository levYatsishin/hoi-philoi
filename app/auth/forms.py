from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo

__all__ = ['LoginForm', 'RegisterForm']


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()], id='sign_form')
    password = PasswordField('password', validators=[DataRequired()], id='sign_form')
    submit = SubmitField("login", id='sign_form')


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()], id='sign_form')
    username = StringField('username', validators=[DataRequired()], id='sign_form')
    mail = EmailField('mail', validators=[DataRequired(), Email()], id='sign_form')
    password = PasswordField('password',
                             validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match!')],
                             id='sign_form')
    password_confirm = PasswordField('password_confirm', validators=[DataRequired()], id='sign_form')
    submit = SubmitField("register", id='sign_form')
