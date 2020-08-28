import os
from flask import Flask, render_template, redirect, url_for, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)


# config
app.config['SECRET_KEY'] = 'onlyfortest'
app.config['UPLOAD_DIR'] = os.path.join(basedir, 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# extensions
db = SQLAlchemy(app)
login_manger = LoginManager(app)
migrate = Migrate(app, db)


# models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile_path = db.Column(db.String(255))


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    file_path = db.Column(db.String(250),nullable=False)
    
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():

    form = VideoForm()
    
    # only for test
    category = [
        (1, 'Film & Animation'),
        (2, 'Autos & Vehicles'),
        (3, 'Music'),
        (4, 'Pets & Animals'),
        (5, 'Sports'),
        (6, 'Travel & Events'),
        (7, 'Gaming'),
        (8, 'People & Blogs'),
        (9, 'Comedy'),
        (10, 'Entertainment'),
        (11, 'News & Politics'),
        (12, 'Howto & Style'),
        (13, 'Education'),
        (14, 'Science & Technology'),
        (15, 'Nonprofits & Activism')
    ]
    form.category.choices = category


    return render_template('upload.html', form=form)


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/signin')
def signin():
    form = SigninForm()

    return render_template('signin.html', form=form)


@app.route('/signup')
def signup():
    form = SignupForm()

    return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/settings')
def settings():
    userForm = UserUpdateForm()
    passwordForm = PasswordUpdateForm()


    return render_template('settings.html', 
        userForm=userForm, 
        passwordForm=passwordForm
    )


@app.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html')


@app.route('/watch')
def watch():
    return render_template('watch.html')


@app.route('/trending')
def trending():
    return render_template('trending.html')


@app.route('/likedVideos')
def likedVideos():
    return render_template('likedVideos.html')


@app.route('/editVideos')
def editVideos():
    return render_template('editVideo.html')


@app.route('/uploads/<path:filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)



# ajax
@app.route('/postComment', methods=['POST'])
def postComment():
    return render_template('comment.html', content=request.form)


if __name__ == '__main__':
    app.run(debug=True)
