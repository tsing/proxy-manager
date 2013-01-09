import gevent.monkey; gevent.monkey.patch_all()
import gevent.queue
import os

from bottle import default_app, route, post, delete, run, request, debug, url, redirect, template, static_file
from auth import require_auth
from store import Store
from flash import FlashPlugin
from middleware import MethodRewrite
from fanout import Fanout

COOKIE_SECRET = "goodgoodstudy"

app = default_app()
app.install(FlashPlugin(COOKIE_SECRET))
flash = app.flash
get_flashed_messages = app.get_flashed_messages
url = app.get_url
fanout = Fanout()

@route ('/domains/wait')
def wait():
    body = gevent.queue.Queue()
    def notify():
        print("ddd")
        if fanout.get(60):
            body.put('update')
        body.put(StopIteration)
    gevent.spawn(notify)
    return body

@route('/')
@require_auth
def index():
    return redirect(url('domains'))

@route('/domains/', name='domains')
@require_auth
def domain_list():
    store = Store()
    domains = store.index()
    if request.headers.get('Accept') == 'text/plain':
        return template('domains.text', domains=domains)
    else:
        return template('domains.html', domains=domains, url=url,
            flashed_messages = get_flashed_messages())

@post('/domains/')
@require_auth
def create_domain():
    domain = request.forms.domain
    if domain:
        store = Store()
        store.create(domain)
        flash("%s added" % domain)
        fanout.update()
    return redirect(url('domains'))

@delete('/domains/<domain>', name='domain_delete')
@require_auth
def delete_domain(domain):
    store = Store()
    store.delete(domain)
    flash("%s deleted" % domain)
    fanout.update()
    return redirect(url('domains'))

@route('/static/<path:path>')
def static(path):
    return static_file(path, os.path.join(os.path.dirname(__file__), "static"))

def main():
    from werkzeug.debug import DebuggedApplication

    app.catchall = False
    wrapped = MethodRewrite(app)
    wrapped = DebuggedApplication(wrapped, evalex=True)
    debug(True)
    run(app=wrapped, reloader=True, server="gevent")

if __name__ == '__main__':
    main()
