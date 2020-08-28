from app import app, db
from flask import render_template, redirect, url_for, send_from_directory, jsonify, request
from models import User
from forms import VideoForm, UserUpdateForm, SigninForm, SignupForm, PasswordUpdateForm
from flask_login import login_required, current_user, logout_user, login_user


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
