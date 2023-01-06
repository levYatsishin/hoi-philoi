from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo

__all__ = ['LoginForm', 'RegisterForm']


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("login")


class RegisterForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    mail = EmailField('mail', validators=[DataRequired(), Email()])
    password = PasswordField('password',
                             validators=[DataRequired(), EqualTo('password_confirm', message='Passwords must match!')])
    password_confirm = PasswordField('password_confirm', validators=[DataRequired()])
    submit = SubmitField("register")
