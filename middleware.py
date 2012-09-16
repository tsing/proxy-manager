from urlparse import parse_qs

class MethodRewrite:

    allowed = ('PUT', 'DELETE')

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if '_method' in environ.get('QUERY_STRING', ''):
            qs = parse_qs(environ.get('QUERY_STRING'))
            methods = qs.get('_method', [])
            if len(methods) == 1 and methods[0] in self.allowed:
                environ['REQUEST_METHOD'] = methods[0]
        return self.app(environ, start_response)
