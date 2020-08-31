import os
import subprocess
from math import floor
from ..extensions import db, login_manager
from . import auth
from flask import render_template, redirect, url_for, send_from_directory, jsonify, request, current_app, flash
from ..models import User, Video, Category, Thumbnail
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

        flash('Invalid email or password.')

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
        flash('You have signed up your account. Thanks!')
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

            # You can only upload mp4!!!!

            #tempFilename = uuid4().hex # create unique filename
            #tempPath = os.path.join(current_app.config['UPLOAD_VIDEO_DIR'], tempFilename)

            #form.video.data.save(tempPath)

            filename = uuid4().hex + '.mp4'
            finalPath = os.path.join(current_app.config['UPLOAD_VIDEO_DIR'], filename)
            form.video.data.save(finalPath)

            # transform videos to mp4
            #cmd = "{} -i {} {}".format(current_app.config['FFMPEG_PATH'], tempPath, finalPath)
            #output = subprocess.run(cmd, shell=True)

            # remove temp file
            #os.remove(tempPath)

            # get the duration
            cmd = "{} -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}".format(current_app.config['FFPROBE_PATH'], finalPath)
            output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

            duration_secs = round(float(output.stdout.decode().rstrip()))

            # transform the duration to hours, minutes and seconds
            hours = duration_secs // 3600
            mins = (duration_secs-hours*3600) // 60
            secs = duration_secs % 60

            duration = timedelta(hours=hours, minutes=mins, seconds=secs)


            # create thumbnails (config)
            thumbnailFilename = uuid4().hex + '.jpg'
            thumbnailPath = os.path.join(current_app.config['UPLOAD_THUMBNAIL_DIR'], thumbnailFilename)
            interval = round(duration_secs * 0.4)
            thumbnailSize = "210x118"

            cmd = "{} -i {} -ss {} -s {} -vframes 1 {}".format(current_app.config['FFMPEG_PATH'], finalPath, interval, thumbnailSize, thumbnailPath)
            output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)

            video.duration = duration
            video.file_path = finalPath
            video.file_url = url_for('page.uploads', filepath=f'videos/{filename}')
            db.session.add(video)
            db.session.commit()

            thumbnail = Thumbnail(
                file_path=thumbnailPath,
                file_url=url_for('page.uploads', filepath=f'thumbnails/{thumbnailFilename}'),
                is_used=True,
                video=video,
            )
            db.session.add(thumbnail)
            db.session.commit()

        flash('A new video has been uploaded.')
        return redirect(url_for('page.index'))

    return render_template('upload.html', form=form)


@auth.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html')