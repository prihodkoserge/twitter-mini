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




# Composite pattern
# Allows to represent posts as single entity
class PostComponent(object):
    def __init__(self):
        pass

    def get_dict(self):
        pass


# Post model
class Post(db.Model, PostComponent):
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


class PostComposite(PostComponent):
    def __init__(self, children=None):
        if children is None:
            self.__children = []
        else:
            self.__children = children

    def append(self, child):
        self.__children.append(child)

    def remove_child(self, child):
        self.__children.remove(child)

    def get_dict(self):
        return [child.get_dict() for child in self.__children]



# Follower model
class Follower(db.Model):
    __tablename__ = 'follower'

    id = db.Column(db.Integer, primary_key=True)
    who_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    whom_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, who, whom):
        self.who_id = who
        self.whom_id = whom




# Uploaded file model
class UploadedFile(db.Model):
    __tablename__ = 'uploaded_file'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    filename = db.Column(db.String(255), unique=True)

    def __init__(self, filename):
        self.filename = filename
