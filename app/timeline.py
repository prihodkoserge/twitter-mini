from app.models import *
from app.app_facade import AppFacade

app_facade = AppFacade()


# User wall model
class Wall:
    def __init__(self, user):
        self.user = user
        self._followers = Follower.query.\
            filter_by(whom_id=user.id).all()

    def posts(self):
        return app_facade.get_user_posts(self.user)

    def add_follower(self, follower):
        if follower is None:
            raise AssertionError
        f = Follower(self.user.id, follower.id)
        db.session.add(f)
        db.session.commit()



# Timeline : 'Factory' pattern
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

    def sorted(self):
        raise NotImplementedError


# Product
class UserTimeline(TimelineInterface):
    def __init__(self, user_id):
        self.user = User.query.get(user_id)

    def block_posts_from_user(self, blocked_user):
        Follower\
            .query\
            .filter_by(who_id=self.user.id, whom_id=blocked_user.id)\
            .delete()
        db.session.commit()

    def get_followings(self):
        f = Follower\
            .query\
            .filter_by(who_id=self.user.id)\
            .all()

        posts = Post.query.all()

        return [post for post in posts if post.user_id in [a.whom_id for a in f]]
        # return Post.query.filter(Post.user_id in [a.whom_id for a in f]).all()

    def posts(self):
        return self.get_followings()


# Product
class PublicTimeline(TimelineInterface):
    def posts(self):
        return app_facade.get_all_posts()

    def sorted(self):
        return app_facade.get_all_posts().sort()