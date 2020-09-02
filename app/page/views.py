import os
import subprocess
from math import floor
from . import page
from ..extensions import db
from flask import render_template, redirect, url_for, send_from_directory, jsonify, request, current_app, abort
from flask_login import login_required, current_user
from ..models import User, Video, Category, LikeVideo, DislikeVideo, Comment, LikeComment, DislikeComment, Subscription
from sqlalchemy import text


@page.route('/')
def index():

    if current_user.is_authenticated:
        sub_videos = Video.query.join(Subscription, Subscription.subscribed_id == Video.user_id).all()
    else:
        sub_videos = None

    videos = Video.query.all()

    return render_template('index.html', videos=videos, sub_videos=sub_videos)


@page.route('/search')
def search():

    if request.args.get('term'):

        search = "%{}%".format(request.args.get('term'))

        temp_query = Video.query.filter(Video.title.ilike(search))

        if request.args.get('orderBy') == 'uploadDate':
            videos = temp_query.order_by(Video.created_at).all()
        else:
            videos = temp_query.order_by(Video.num_views).all()

    
        return render_template('search.html', videos=videos, term=request.args.get('term'))
    

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


@page.route('/subscriptions')
@login_required
def subscriptions():

    videos = Video.query.join(Subscription, Subscription.subscribed_id == Video.user_id).all()
    return render_template('subscriptions.html', videos=videos)


@page.route('/trending')
def trending():

    time_interval = text("NOW() - INTERVAL '7 DAYS'")
    videos = Video.query.filter(Video.created_at > time_interval).limit(15).all()

    return render_template('trending.html', videos=videos)


@page.route('/likedVideos')
@login_required
def likedVideos():

    videos = Video.query.join(LikeVideo, LikeVideo.video_id == Video.id).filter(LikeVideo.user_id == current_user.id).all()

    return render_template('likedVideos.html', videos=videos)


@page.route('/uploads/<path:filepath>')
def uploads(filepath):
    return send_from_directory(current_app.config['UPLOAD_DIR'], filepath)


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


@page.route('/subscribe', methods=['POST'])
@login_required
def subscribe():

    subscriber_id = request.form['userFrom']
    subscribed_id = request.form['userTo']

    subscription = Subscription.query.filter_by(subscriber_id=subscriber_id, subscribed_id=subscribed_id).first()
    if subscription:
        db.session.delete(subscription)
        db.session.commit()
    else:
        subscription = Subscription(
            subscriber_id=subscriber_id,
            subscribed_id=subscribed_id,
        )
        db.session.add(subscription)
        db.session.commit()
        
    count = Subscription.query.filter_by(subscribed_id=subscribed_id).count()

    return str(count) 


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
        like = LikeComment.query.filter_by(user_id=current_user.id, comment_id=comment.id).first()
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
