from functools import wraps
from bottle import request, HTTPError

def check_auth(username, password):
    return username == 'tsing' and password == 'geowhy'

def authenticate():
    raise HTTPError(401, 'Login Required', header=
        (('WWW-Authenticate', 'Basic realm="login"'),))

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.auth
        if not auth:
            return authenticate()
        elif not check_auth(auth[0], auth[1]):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
