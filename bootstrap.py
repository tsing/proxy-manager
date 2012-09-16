#!/usr/bin/env python
from domains import app
from middleware import MethodRewrite, SchemeRewrite
from bottle import run
import sys

app = SchemeRewrite(MethodRewrite(app))

def main():
    port = sys.argv[1]
    run(server="gevent", port=port, app=app)

if __name__ == '__main__':
    main()
