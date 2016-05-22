from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    files = db.relationship('UploadedFile', backref='post', lazy='dynamic')

    def __init__(self, user_id, timestamp, content):
        self.user_id = user_id
        self.timestamp = timestamp
        self.content = content

    def get_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'timestamp': self.timestamp
        }

    @staticmethod
    def list_for_user(user_id):
         return [
             post.get_dict() for post in
             Post.query.filter_by(user_id=user_id)
         ]


class Follower(db.Model):
    __tablename__ = 'follower'

    id = db.Column(db.Integer, primary_key=True)
    who_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    whom_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, who, whom):
        self.who_id = who
        self.whom_id = whom


class UploadedFile(db.Model):
    __tablename__ = 'uploaded_file'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), unique=True)

    def __init__(self, user_id, post_id, filename):
        self.user_id = user_id
        self.post_id = post_id
        self.filename = filename


# Factory
class Timeline(object):
    @staticmethod
    def get(user_id=None):
        if user_id is not None:
            return UserTimeline(user_id)
        else:
            return PublicTimeline()


# Product
class UserTimeline():
    def __init__(self, user_id):
        self.user = User.query.get(user_id)

    def posts(self):
        return [post for post in self.user.posts]


# Product
class PublicTimeline():
    def posts(self):
        return [post for post in Post.query.all()];