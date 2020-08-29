import os
import subprocess
from math import floor
from . import page
from ..extensions import db
from flask import render_template, redirect, url_for, send_from_directory, jsonify, request, current_app
from ..models import User, Video, Category


@page.route('/')
def index():
    return render_template('index.html')


@page.route('/search')
def search():
    return render_template('search.html')


@page.route('/profile/<username>')
def profile(username):

    user = User.query.filter_by(username=username).first()

    videos = user.videos.order_by(Video.created_at).all()

    return render_template('profile.html', user=user, videos=videos)


@page.route('/watch')
def watch():
    return render_template('watch.html')


@page.route('/trending')
def trending():
    return render_template('trending.html')


@page.route('/likedVideos')
def likedVideos():
    return render_template('likedVideos.html')


@page.route('/editVideos')
def editVideos():
    return render_template('editVideo.html')


@page.route('/uploads/<path:filepath>')
def uploads(filepath):
    return send_from_directory(current_app.config['UPLOAD_DIR'], filepath)


# ajax
@page.route('/postComment', methods=['POST'])
def postComment():
    return render_template('comment.html', content=request.form)
