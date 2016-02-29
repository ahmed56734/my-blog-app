from flask_wtf import Form
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from flask.ext.wtf.html5 import URLField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,\
    url, ValidationError

from models import User

class PostForm(Form):
    title = StringField('Post title:', validators=[DataRequired()])
    content = TextAreaField('Post content:', validators=[DataRequired()])


class LoginForm(Form):
    username = StringField('Your Username:', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')

class SignupForm(Form):
    username = StringField('Username',
                    validators=[
                        DataRequired(), Length(3, 80),
                        Regexp('^[A-Za-z0-9_]{3,}$',
                            message='Usernames consist of numbers, letters,'
                                    'and underscores.')])
    password = PasswordField('Password',
                    validators=[
                        DataRequired(),
                        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_username(self, username_field):
        if User.query.filter_by(username=username_field.data).first():
            raise ValidationError('This username is already taken.')
