from .extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash


# models
class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    subscribed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #file_path = db.Column(db.String(255))

    videos = db.relationship('Video', backref='user', lazy='dynamic')
    like_videos = db.relationship('LikeVideo', backref='user', lazy='dynamic')
    dislike_videos = db.relationship('DislikeVideo', backref='user', lazy='dynamic')
    like_comments = db.relationship('LikeComment', backref='user', lazy='dynamic')
    dislike_comments = db.relationship('DislikeComment', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')

    subscribed_by = db.relationship(
        'Subscription',
        foreign_keys=[Subscription.subscriber_id],
        backref=db.backref('subscriber', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    subscribers = db.relationship(
        'Subscription',
        foreign_keys=[Subscription.subscribed_id],
        backref=db.backref('subscribed', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan'
    )

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    is_private = db.Column(db.Boolean, default=False)
    file_path = db.Column(db.String(255), nullable=False, unique=True)
    file_url = db.Column(db.String(255), nullable=False, unique=True)
    duration = db.Column(db.Interval, default=timedelta())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    num_views = db.Column(db.Integer, default=0)
    
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    thumbnails = db.relationship('Thumbnail', backref='video', lazy='dynamic')
    liked_by = db.relationship('LikeVideo', backref='video', lazy='dynamic')
    disliked_by = db.relationship('DislikeVideo', backref='video', lazy='dynamic')
    comments = db.relationship('Comment', backref='video', lazy='dynamic')


    # very easy way to increase views
    def increment_views(self):
        self.num_views += 1

        db.session.add(self)
        db.session.commit()

        return None


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


    videos = db.relationship('Video', backref='category', lazy='dynamic')

    @staticmethod
    def insert_category():
        categories = [
            'Film & Animation',
            'Autos & Vehicles',
            'Music',
            'Pets & Animals',
            'Sports',
            'Travel & Events',
            'Gaming',
            'People & Blogs',
            'Comedy',
            'Entertainment',
            'News & Politics',
            'Howto & Style',
            'Education',
            'Science & Technology',
            'Nonprofits & Activism',
        ]
        for c in categories:
            category = Category.query.filter_by(name=c).first()
            if category is None:
                category = Category(name=c)
            db.session.add(category)
        
        db.session.commit()


class Thumbnail(db.Model):
    __tablename__ = 'thumbnails'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False, unique=True)
    file_url = db.Column(db.String(255), nullable=False, unique=True)
    is_used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('comments.id'))


    liked_by = db.relationship('LikeComment', backref='comment', lazy='dynamic')
    disliked_by = db.relationship('DislikeComment', backref='comment', lazy='dynamic')


class LikeVideo(db.Model):
    __tablename__ = 'like_videos'

    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DislikeVideo(db.Model):
    __tablename__ = 'dislike_videos'

    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LikeComment(db.Model):
    __tablename__ = 'like_comments'

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DislikeComment(db.Model):
    __tablename__ = 'dislike_comments'

    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
