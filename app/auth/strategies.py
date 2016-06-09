from app.models import User
# from werkzeug.contrib import

class AuthenticationStrategy(object):
    def check_auth(self, request):
        raise NotImplementedError


class HttpBasicAuthenticationStrategy(AuthenticationStrategy):
    def check_auth(self, request):
        auth_data = request.authorization
        if not auth_data:
            return False
        user = User.query.filter_by(email=auth_data.username).first()
        if user is not None and user.check_password(auth_data.password):
            return user
        return False


class HttpDigestAuthenticationStrategy(AuthenticationStrategy):
    def __init__(self):
        return

