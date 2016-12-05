import sys
sys.path.insert(0, '../')

import weakref

from lib.sinon.SinonStub import SinonStub
from lib.sinon.util import ErrorHandler, Wrapper, CollectionHandler

class SinonExpectation(SinonStub):

    def __init__(self, obj=None, prop=None):
        super(SinonExpectation, self).__init__(obj, prop)
        self.valid_list = []

    def atLeast(self, n):
        def fn():
            return True if n <= super(SinonExpectation, self).callCount else False
        self.valid_list.append(fn)
        return self

    def atMost(self, n):
        def fn():
            return True if n >= super(SinonExpectation, self).callCount else False
        self.valid_list.append(fn)
        return self

    def never(self):
        def fn():
            return not super(SinonExpectation, self).called
        self.valid_list.append(fn)
        return self

    def once(self):
        def fn():
            return super(SinonExpectation, self).calledOnce
        self.valid_list.append(fn)
        return self

    def twice(self):
        def fn():
            return super(SinonExpectation, self).calledTwice
        self.valid_list.append(fn)
        return self

    def thrice(self):
        def fn():
            return super(SinonExpectation, self).calledThrice
        self.valid_list.append(fn)
        return self

    def exactly(self, n):
        def fn():
            return True if n == super(SinonExpectation, self).callCount else False
        self.valid_list.append(fn)
        return self

    def withArgs(self, *args, **kwargs):
        def fn():
            return super(SinonExpectation, self).calledWith(*args, **kwargs)
        self.valid_list.append(fn)
        return self

    def withExactArgs(self, *args, **kwargs):
        def fn():
            return super(SinonExpectation, self).calledWithExactly(*args, **kwargs)
        self.valid_list.append(fn)
        return self

    def on(self, obj):
        pass

    def verify(self):
        valid = True
        for fn in self.valid_list:
            valid = valid & fn()
        return valid


class SinonMock(object):

    _queue = []

    def __new__(self, obj=None):
        new = super(SinonMock, self).__new__(self)
        self._queue.append(new)
        new.__init__(obj)
        return weakref.proxy(new)

    def __init__(self, obj=None):
        self.obj = obj
        self.exp_list = []

    def expects(self, prop):
        expectation = SinonExpectation(self.obj, prop)
        self.exp_list.append(expectation)
        return expectation

    def verify(self):
        for expectation in self.exp_list:
            try:
                if hasattr(expectation, "verify") and not expectation.verify():
                    return False
            except ReferenceError:
                pass #ignore removed expectation
        return True

    def restore(self):
        for expectation in self.exp_list:
            try:
                expectation.restore()
            except ReferenceError:
                pass #ignore removed expectation
        self._queue.remove(self)
