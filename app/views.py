import os
from flask import render_template, request
from werkzeug.utils import secure_filename
from app import app
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from app.models import Timeline

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
def index():

    return render_template("timeline.html",
                           timeline=Timeline.get().posts())


@app.route("/up", methods=["GET", "POST"])
def upload():
    args = {"method": "GET"}
    if request.method == "POST":
        file = request.files["file"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            args["method"] = "POST"
    return render_template("upload.html", args=args)