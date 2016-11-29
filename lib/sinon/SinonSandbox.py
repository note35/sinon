def sinontest(f):
    def fn(*args, **kwargs):
        ret = f(*args, **kwargs)
        if "SinonSpy" in f.__globals__.keys():
            for item in f.__globals__["SinonSpy"]._queue:
                item.restore()
        if "SinonStub" in f.__globals__.keys():
            for item in f.__globals__["SinonStub"]._queue:
                item.restore()
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
