properties = ["SinonSpy", "SinonStub", "SinonMock"]

def _clear_item_in_queue(queue):
    for item in queue:
        item.restore()


def sinontest(f):
    def fn(*args, **kwargs):
        ret = f(*args, **kwargs)
        for prop in properties:
            if prop in f.__globals__.keys():
                _clear_item_in_queue(f.__globals__[prop]._queue)
        return ret
    return fn


class SinonSandbox(object):

    def __init__(self):
        pass

    def create(self, config=None):
        pass

    def spy(self):
        pass

    def stub(self):
        pass

    def mock(self):
        pass

    def restore(self):
        pass
