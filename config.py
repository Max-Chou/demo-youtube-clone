import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e7f7d5db0e0f4e068da84d44b38cb2f7'

    UPLOAD_DIR = os.environ.get('UPLOAD_DIR') or os.path.join(basedir, 'uploads')
    UPLOAD_VIDEO_DIR = os.environ.get('UPLOAD_VIDEO_DIR') or os.path.join(basedir, 'uploads', 'videos')
    UPLOAD_PROFILE_DIR = os.environ.get('UPLOAD_PROFILE_DIR') or os.path.join(basedir, 'uploads', 'profiles')
    UPLOAD_THUMBNAIL_DIR = os.environ.get('UPLOAD_THUMBNAIL_DIR') or os.path.join(basedir, 'uploads', 'thumbnails')

    FFMPEG_PATH = os.path.join(basedir, 'ffmpeg')
    FFPROBE_PATH = os.path.join(basedir, 'ffprobe')

    #ALLOWED_VIDEOS = {"mp4", "flv", "webm", "mkv", "vob", "ogv", "ogg", "avi", "wmv", "mov", "mpeg", "mpg"}
    ALLOWED_VIDEOS = {"mp4"}
    # ALLOWED_IMAGES = 

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}