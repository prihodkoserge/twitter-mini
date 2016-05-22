import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

UPLOAD_FOLDER = os.path.join(basedir, 'files/uploads')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg', 'mp3', 'mp4', 'avi', 'mpeg'])