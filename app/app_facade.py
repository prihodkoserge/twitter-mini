from app import db
from app.models import Post, PostComposite, User, UploadedFile


# Interface to hide implementation details
# Actually, 'Facade' pattern
class AppFacade(object):
    def __init__(self):
        self.post_model = Post
        self.user_model = User
        self.file_model = UploadedFile

    def get_all_posts(self):
        return self.post_model\
            .query\
            .order_by(Post.timestamp.desc())\
            .all()

    def API_get_all_posts(self):
        res = self.post_model\
            .query\
            .order_by(Post.timestamp.desc())\
            .all()
        return PostComposite(children=res)

    def get_posts_from_period(self, ts):
        return self.post_model\
            .query\
            .filter_by(timestamp=ts)\
            .all()

    def get_user_posts(self, user):
        return self.post_model\
            .query\
            .filter_by(user_id=user.id)\
            .order_by(Post.timestamp.desc())\
            .all()

    def get_user_posts_by_id(self, user_id):
        return self.post_model\
            .query\
            .filter_by(user_id=user_id)\
            .all()

    def get_all_files(self):
        return self.file_model\
            .query\
            .all()

    def get_post_files(self, post):
        return post.files

    def get_post_files_by_id(self, post_id):
        return self.file_model\
            .query\
            .filter_by(post_id=post_id)\
            .all()

    def remove_post(self, post):
        if post is not None:
            db.session.delete(post)
            db.session.commit()

    def remove_user(self, user):
        if user is not None:
            db.session.delete(user)
            db.session.commit()

    def add_follower(self, follower):
        db.session.add(follower)
        db.session.commit()
