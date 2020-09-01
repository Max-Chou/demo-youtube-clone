import os
import subprocess
from math import floor
from . import page
from ..extensions import db
from flask import render_template, redirect, url_for, send_from_directory, jsonify, request, current_app, abort
from flask_login import login_required, current_user
from ..models import User, Video, Category, LikeVideo, DislikeVideo, Comment, LikeComment, DislikeComment


@page.route('/')
def index():
    return render_template('index.html')


@page.route('/search')
def search():
    return render_template('search.html')


@page.route('/profile/<username>')
@page.route('/profile/<int:id>')
def profile(username=None, id=None):

    user = None
    if username:
        user = User.query.filter_by(username=username).first()

    if id:
        user = User.query.get(id)

    if not user:
        abort(404)

    videos = user.videos.order_by(Video.created_at).all()

    return render_template('profile.html', user=user, videos=videos)


@page.route('/watch/<int:id>')
def watch(id):
    video = Video.query.get(id)
    video.increment_views()

    comments = video.comments.filter(Comment.reply_id == None).order_by(Comment.created_at.desc())
    replies = video.comments.filter(Comment.reply_id != None)

    return render_template('watch.html', video=video, comments=comments, replies=replies)


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

    comment = Comment(
        body=request.form['commentText'],
        user_id=request.form['userId'],
        video_id=request.form['videoId']
    )

    if request.form.get('responseTo'):
        comment.reply_id = request.form.get('responseTo')

    db.session.add(comment)
    db.session.commit()

    video = Video.query.get(request.form['videoId'])
    replies = video.comments.filter(Comment.reply_id != None)

    return render_template('comment.html', comment=comment, replies=replies)


@page.route('/getCommentReplies', methods=['POST'])
def getCommentReplies():
    replies = Comment.query.filter_by(video_id=request.form['videoId'], reply_id=request.form['commentId'])

    return render_template('reply.html', replies=replies)

@page.route('/likeVideo', methods=['POST'])
@login_required
def likeVideo():

    video_id = request.form['videoId']

    video = Video.query.get(video_id)
    user = video.liked_by.filter_by(user_id=current_user.id).first()
    if user:
        like = LikeVideo.query.filter_by(user_id=current_user.id, video_id=video.id).first()
        db.session.delete(like)
        db.session.commit()
        result = {
            "likes": -1,
            "dislikes": 0
        }
    else:
        dislike = DislikeVideo.query.filter_by(user_id=current_user.id, video_id=video.id).first()
        if dislike:
            count = -1
            db.session.delete(dislike)
            db.session.commit()
        else:
            count = 0

        like = LikeVideo(
            video_id=video_id,
            user_id=current_user.id,
        )
        db.session.add(like)
        db.session.commit()
        result = {
            "likes": 1,
            "dislikes": count
        }

    return jsonify(result)

@page.route('/dislikeVideo', methods=['POST'])
@login_required
def dislikeVideo():

    video_id = request.form['videoId']

    video = Video.query.get(video_id)
    user = video.disliked_by.filter_by(user_id=current_user.id).first()
    if user:
        dislike = DislikeVideo.query.filter_by(user_id=current_user.id, video_id=video.id).first()
        db.session.delete(dislike)
        db.session.commit()
        result = {
            "likes": 0,
            "dislikes": -1
        }
    else:
        like = LikeVideo.query.filter_by(user_id=current_user.id, video_id=video.id).first()
        if like:
            count = -1
            db.session.delete(like)
            db.session.commit()
        else:
            count = 0


        dislike = DislikeVideo(
            video_id=video_id,
            user_id=current_user.id,
        )
        db.session.add(dislike)
        db.session.commit()
        result = {
            "likes": count,
            "dislikes": 1
        }

    return jsonify(result)

@page.route('/likeComment', methods=['POST'])
@login_required
def likeComment():

    comment_id = request.form['commentId']
    video_id = request.form['videoId']

    comment = Comment.query.filter_by(id=comment_id, video_id=video_id).first()
    user = comment.liked_by.filter_by(user_id=current_user.id).first()
    if user:
        like = LikeComment.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
        db.session.delete(like)
        db.session.commit()
        
        return str(-1)
    else:
        dislike = DislikeComment.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
        if dislike:
            count = 1
            db.session.delete(dislike)
            db.session.commit()
        else:
            count = 0

        like = LikeComment(
            comment_id=comment.id,
            user_id=current_user.id,
        )
        db.session.add(like)
        db.session.commit()
        
        return str(1 + count)


@page.route('/dislikeComment', methods=['POST'])
@login_required
def dislikeComment():

    comment_id = request.form['commentId']
    video_id = request.form['videoId']

    comment = Comment.query.filter_by(id=comment_id, video_id=video_id).first()
    user = comment.disliked_by.filter_by(user_id=current_user.id).first()
    if user:
        dislike = DislikeComment.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
        db.session.delete(dislike)
        db.session.commit()

        return str(1)
    else:
        like = DislikeComment.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
        if like:
            count = 1
            db.session.delete(like)
            db.session.commit()
        else:
            count = 0


        dislike = DislikeComment(
            comment_id=comment_id,
            user_id=current_user.id,
        )
        db.session.add(dislike)
        db.session.commit()

        return str(-1 - count)
