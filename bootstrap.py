#!/usr/bin/env python
from domains import app
from middleware import MethodRewrite, SchemeRewrite
from bottle import run
import sys

app = SchemeRewrite(MethodRewrite(app))

def main():
    host = sys.argv[1]
    port = sys.argv[2]
    run(server="gevent", host=host, port=port, app=app)

if __name__ == '__main__':
    main()
