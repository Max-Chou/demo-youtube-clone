import os
from flask import Flask, render_template, redirect, url_for, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


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

# view functions
from views import *





if __name__ == '__main__':
    app.run(debug=True)
