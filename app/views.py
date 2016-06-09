import os
from datetime import datetime
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app import app, db
from app import forms
from flask import render_template, request, abort
from werkzeug.utils import secure_filename
from app.models import *
from app.auth.decorator import CheckAuthDecorator
from app.auth.strategies import HttpBasicAuthenticationStrategy


basic_auth = HttpBasicAuthenticationStrategy()
requires_auth = CheckAuthDecorator(auth_strategy=basic_auth)


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
    return render_template(
        "wall.html",
        wall=Wall(user)
    )

