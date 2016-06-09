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
        # return check_password_hash(self.password, password)
        return self.password == password

    @staticmethod
    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    files = db.relationship('UploadedFile', backref='post', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, timestamp, content):
        self.timestamp = timestamp
        self.content = content

    def get_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user.id,
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
    filename = db.Column(db.String(255), unique=True)

    def __init__(self, filename):
        self.filename = filename


class Wall:
    def __init__(self, user):
        self.user = user
        self._followers = Follower.query.filter_by(whom_id=user.id)

    def posts(self):
        return [post for post in self.user.posts]

    def add_follower(self, follower):
        if follower is None:
            raise AssertionError
        f = Follower(self.user.id, follower.id)
        db.session.add(f)
        db.session.commit()




# Factory
class Timeline(object):
    @staticmethod
    def get(user_id=None):
        if user_id is not None:
            return UserTimeline(user_id)
        else:
            return PublicTimeline()


class TimelineInterface():

    def posts(self):
        raise NotImplementedError

    def sort(self):
        raise NotImplementedError


# Product
class UserTimeline(TimelineInterface):
    def __init__(self, user_id):
        self.user = User.query.get(user_id)

    def posts(self):
        return [post for post in self.user.posts]


# Product
class PublicTimeline(TimelineInterface):
    def posts(self):
        return [post for post in Post.query.all()]