import os
from flask import Flask, render_template, redirect, url_for, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm

basedir = os.path.abspath(os.path.dirname(__name__))
app = Flask(__name__)

app.config['SECRET_KEY'] = 'onlyfortest'
app.config['UPLOAD_DIR'] = os.path.join(basedir, 'uploads')

# models




# forms




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))


@app.route('/settings')
def settings():
    return render_template('settings.html')


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


if __name__ == '__main__':
    app.run(debug=True)
