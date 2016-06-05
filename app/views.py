import os
from flask import render_template, request, Response
from werkzeug.utils import secure_filename
from app import app
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app.models import Timeline
from app import forms
from functools import wraps
from app.auth.strategies import HttpBasicAuthenticationStrategy


basic_auth = HttpBasicAuthenticationStrategy()


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def check_auth(username, password):
    return username=='aaa' and password=='bbb'


def authenticate():
    return Response(
        'Could not verify your access level for that URL', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required'}
    )


# Decorator
# Wraps view method and decorate it
# with adding authentication requirements

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not basic_auth.check_auth(request):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/', methods=["GET", "POST"])
@requires_auth
def index():
    tweet_form = forms.TweetForm(request.form)
    if tweet_form.is_submitted():
        print("Submitter")
    return render_template("timeline.html",
                           timeline=Timeline.get().posts(),
                           tweet_form=forms.TweetForm()
                           )


@app.route("/up", methods=["GET", "POST"])
def upload():
    args = {"method": "GET"}
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            args["method"] = "POST"
    return render_template("upload.html", args=args, tweet_form=forms.TweetForm)