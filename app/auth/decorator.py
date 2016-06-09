from flask import Response, request
from functools import wraps


class CheckAuthDecorator:
    def __init__(self, auth_strategy):
        self.auth_strategy = auth_strategy

    def __call__(self, fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            if not self.auth_strategy.check_auth(request):
                return self.authenticate()
            return fn(*args, **kwargs)
        return decorated

    def authenticate(self):
        return Response(
            'Could not verify your access level for that URL', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required'}
        )
