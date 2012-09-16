from domains import app
from middleware import MethodRewrite

app = MethodRewrite(app)
