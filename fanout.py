import gevent.event

class Fanout:

    def __init__(self):
        self.event = gevent.event.AsyncResult()

    def get(self, timeout):
        try:
            self.event.get(block=True, timeout=timeout)
            return True
        except:
            return False

    def update(self):
        self.event.set()
        self.event = gevent.event.AsyncResult()
