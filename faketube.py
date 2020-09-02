import os
import click
from flask.cli import AppGroup
from flask_migrate import Migrate
from app import create_app
from app.extensions import db, login_manager
from app.models import User, Video, Category, Thumbnail, LikeVideo, DislikeVideo, \
    Comment, LikeComment, DislikeComment, Subscription

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db) # this will fix alter in sqlite

category_cli = AppGroup('category')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Video=Video, Category=Category, Thumbnail=Thumbnail,
                LikeVideo=LikeVideo, DislikeVideo=DislikeVideo, Comment=Comment,
                LikeComment=LikeComment, DislikeComment=DislikeComment, 
                Subscription=Subscription)


@category_cli.command('init')
def init_category(name):
    Category.insert_category()


@category_cli.command('create')
@click.argument('name')
def create_category(name):
    c = Category.query.filter_by(name=name).first()
    if c is None:
        c = Category(name=name)
        db.session.add(c)
        db.session.commit()


app.cli.add_command(category_cli)