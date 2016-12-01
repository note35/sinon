import sys
sys.path.insert(0, '../')

import weakref

from lib.sinon.SinonBase import SinonBase
from lib.sinon.SinonSpy import SinonSpy
from lib.sinon.util import ErrorHandler, Wrapper, CollectionHandler

class SinonExpectation(SinonSpy):

    def __init__(self, obj=None, prop=None):
        super(SinonSpy, self).__init__(obj, prop)
        self.valid = True

    def atLeast(self, n):
        self.valid = self.valid & (True if n >= super(SinonExpectation, self).callCount else False)
        return self

    def atMost(self, n):
        self.valid = self.valid & (True if n <= super(SinonExpectation, self).callCount else False)
        return self

    def never(self):
        self.valid = self.valid & (not super(SinonExpectation, self).called)
        return self

    def once(self):
        self.valid = self.valid & (super(SinonExpectation, self).calledOnce)
        return self

    def twice(self):
        self.valid = self.valid & (super(SinonExpectation, self).calledTwice)
        return self

    def thrice(self):
        self.valid = self.valid & (super(SinonExpectation, self).calledThrice)
        return self

    def exactly(self, n):
        self.valid = self.valid & (True if n == super(SinonExpectation, self).callCount else False)
        return self

    def withArgs(self, *args, **kwargs):
        self.valid = self.valid & (super(SinonExpectation, self).calledWith(*args, **kwargs))
        return self

    def withExactArgs(self, *args, **kwargs):
        self.valid = self.valid & (super(SinonExpectation, self).calledWithExactly(*args, **kwargs))
        return self

    def on(self, obj):
        pass

    def verify(self):
        return self.valid


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
            if not expectation.valid:
                return False
        return True

    def restore(self):
        for expectation in self.exp_list:
            expectation.restore()
        self._queue.remove(self)
