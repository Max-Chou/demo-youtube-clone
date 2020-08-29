import os
import subprocess
from math import floor
from ..extensions import db, login_manager
from . import auth
from flask import render_template, redirect, url_for, send_from_directory, jsonify, request, current_app
from ..models import User, Video, Category
from ..utils import allowed_file
from .forms import VideoForm, UserUpdateForm, SigninForm, SignupForm, PasswordUpdateForm
from flask_login import login_required, current_user, logout_user, login_user
from uuid import uuid4
from datetime import timedelta


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('page.index')
            return redirect(next)

    return render_template('signin.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data.lower(),
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()
    
        return redirect(url_for('page.index'))
    return render_template('signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('page.index'))


@auth.route('/settings')
def settings():
    userForm = UserUpdateForm()
    passwordForm = PasswordUpdateForm()


    return render_template('settings.html', 
        userForm=userForm, 
        passwordForm=passwordForm
    )


@auth.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():

    form = VideoForm()
    
    items = Category.query.all()
    category = [(item.id, item.name) for item in items]

    # only for test
    #category = [
    #    (1, 'Film & Animation'),
    #    (2, 'Autos & Vehicles'),
    #    (3, 'Music'),
    #    (4, 'Pets & Animals'),
    #    (5, 'Sports'),
    #    (6, 'Travel & Events'),
    #    (7, 'Gaming'),
    #    (8, 'People & Blogs'),
    #    (9, 'Comedy'),
    #    (10, 'Entertainment'),
    #    (11, 'News & Politics'),
    #    (12, 'Howto & Style'),
    #    (13, 'Education'),
    #    (14, 'Science & Technology'),
    #    (15, 'Nonprofits & Activism')
    #]
    form.category.choices = category

    if form.validate_on_submit():

        video = Video(
            title=form.title.data,
            description=form.description.data,
            is_private=form.is_private.data,
            category_id=form.category.data,
            user_id=current_user.id
        )
        
        # process video
        if form.video.data and allowed_file(form.video.data.filename, current_app.config['ALLOWED_VIDEOS']):
            tempFilename = uuid4().hex # create unique filename
            tempPath = os.path.join(current_app.config['UPLOAD_VIDEO_DIR'], tempFilename)

            form.video.data.save(tempPath)

            filename = uuid4().hex + '.mp4'
            finalPath = os.path.join(current_app.config['UPLOAD_VIDEO_DIR'], filename)

            # transform videos to mp4
            cmd = "{} -i {} {}".format(current_app.config['FFMPEG_PATH'], tempPath, finalPath)
            output = subprocess.run(cmd, shell=True)

            # remove temp file
            os.remove(tempPath)

            # get the duration
            cmd = "{} -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}".format(current_app.config['FFPROBE_PATH'], finalPath)
            output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

            duration_secs = round(float(output.stdout.decode().rstrip()))

            # transform the duration to hours, minutes and seconds
            hours = duration_secs // 3600
            mins = (duration_secs-hours*3600) // 60
            secs = duration_secs % 60

            duration = timedelta(hours=hours, minutes=mins, seconds=secs)

            video.duration = duration
            video.file_path = finalPath
            video.file_url = url_for('page.uploads', filepath=f'videos/{filename}')

        db.session.add(video)
        db.session.commit()

        return redirect(url_for('page.index'))

    return render_template('upload.html', form=form)


@auth.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html')