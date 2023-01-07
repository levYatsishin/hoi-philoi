from datetime import date

from flask_wtf import FlaskForm
from wtforms import TextAreaField, DateField, StringField, SubmitField
from wtforms.validators import DataRequired

__all__ = ['Event', 'Post']


class Event(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    image_url = StringField('Image url')
    time_start = DateField('Start Date', default=date.today, validators=[DataRequired()])
    time_end = DateField('Start Date', default=date.today, validators=[DataRequired()])
    locate = StringField('Location', validators=[DataRequired()])
    submit = SubmitField()


class Post(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    image_url = StringField('Image url')
    submit = SubmitField()
