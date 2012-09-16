from domains import app
from middleware import MethodRewrite
from bottle import run
import sys

app = MethodRewrite(app)

def main():
    port = sys.argv[1]
    run(server="gevent", port=port)

if __name__ == '__main__':
    main()
