import os
from datetime import datetime
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from werkzeug.utils import secure_filename

from app import app, db
from app import forms
from app.models import *
from app.auth.decorator import CheckAuthDecorator
from app.auth.strategies import HttpBasicAuthenticationStrategy

from flask import render_template, request, g, \
                    abort, redirect, url_for, flash


basic_auth = HttpBasicAuthenticationStrategy()


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
@CheckAuthDecorator(auth_strategy=basic_auth)
def index():
    tweet_form = forms.TweetForm()
    if tweet_form.validate_on_submit():
        author = basic_auth.check_auth(request)

        if author:
            post = Post(datetime.utcnow(), tweet_form.tweet_content.data)

            if tweet_form.attachment.data:
                uploaded_file = request.files[tweet_form.attachment.name]
                if allowed_file(uploaded_file.filename):
                    filename = secure_filename(uploaded_file.filename)
                    uploaded_file.save(os.path.join(UPLOAD_FOLDER, filename))
                    post.files.append(UploadedFile(filename=filename))

            author.posts.append(post)
            db.session.commit()

    return render_template(
        "timeline.html",
        timeline=Timeline.get().posts(),
        tweet_form=forms.TweetForm()
    )


@app.route('/<username>')
@CheckAuthDecorator(auth_strategy=basic_auth)
def wall(username):
    user = User.get_user_by_username(username)
    if user is None:
        abort(404)

    curr_user = basic_auth.check_auth(request)

    return render_template(
        "wall.html",
        wall=Wall(user),
        curr_user=curr_user.username
    )


@app.route('/wall')
@CheckAuthDecorator(auth_strategy=basic_auth)
def curr_user_wall():
    curr_user = basic_auth.check_auth(request)
    return redirect(url_for('wall', username=g.user.username))


@app.route('/<username>/follow')
@CheckAuthDecorator(auth_strategy=basic_auth)
def follow_user(username):
    return


@app.route('/<username>/unfollow')
@CheckAuthDecorator(auth_strategy=basic_auth)
def unfollow_user(username):
    return
