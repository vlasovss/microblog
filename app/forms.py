from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo 
from wtforms.validators import Length 
from wtforms.validators import ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired()],
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired()],
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()],
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
    )
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired()],
    )
    about_me = TextAreaField(
        'About me',
        validators=[Length(min=0, max=140)]
    )
    submit = SubmitField('Submit')
    
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('The username is busy. \
                    Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')


class PostForm(FlaskForm):
    post = TextAreaField(
        'Say something',
        validators=[DataRequired(), Length(min=1, max=140)]
    )
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()],
    )
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
    )
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')],
    )
    submit = SubmitField('Reauest Password Reset')