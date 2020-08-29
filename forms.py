
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# forms
class VideoForm(FlaskForm):
    video = FileField('Your video', validators=[
        DataRequired()
    ])

    title = StringField('Title', validators=[
        DataRequired(),
        Length(max=70),
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        Length(max=1000),
    ])
    is_private = SelectField('Privacy', coerce=bool, choices=[
        (True, 'Private'),
        (False, 'Public'),
    ])
    category = SelectField('Category', coerce=int)


class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(max=25)
    ])

    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(max=25)
    ])

    username = StringField('Username', validators=[
        DataRequired(),
        Length(max=25)
    ])

    email = StringField('Email', validators=[
        DataRequired(),
        Length(max=100),
        Email(),
        EqualTo('email2', message='Emails must match.')
    ])
    email2 = StringField('Confirm email')
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(8, 16),
        EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm Password')


class SigninForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
    ])

    password = PasswordField('Password', validators=[
        DataRequired()
    ])


class UserUpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(max=25)
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(max=25)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Length(max=100),
        Email()
    ])


class PasswordUpdateForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[
        DataRequired()
    ])
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(8, 16),
        EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm new password', validators=[
        DataRequired(),
    ])