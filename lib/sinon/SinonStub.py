import sys
sys.path.insert(0, '../')

from lib.sinon.util import ErrorHandler, Wrapper, CollectionHandler
from lib.sinon.SinonBase import SinonBase

class SinonStub(SinonBase):

    def __init__(self, obj=None, prop=None, func=None):
        super(SinonStub, self).__init__(obj, prop)
        self.stubfunc = func if func else Wrapper.emptyFunction
        super(SinonStub, self).addWrapStub(self.stubfunc)
        self.condition = {"args":[], "kwargs":[], "action": [], "oncall":[]}
        self.args = self.kwargs = self.oncall = None

    def _appendCondition(self, func):
        self.condition["args"].append(self.args)
        self.condition["kwargs"].append(self.kwargs)
        self.condition["oncall"].append(self.oncall)
        self.condition["action"].append(func)
        self.args = self.kwargs = self.oncall = None

    def withArgs(self, *args, **kwargs):
        if args:
            self.args = args
        if kwargs:
            self.kwargs = kwargs
        return self

    def onCall(self, n):
        self.oncall = n
        return self

    def onFirstCall(self):
        self.oncall = 1
        return self

    def onSecondCall(self):
        self.oncall = 2
        return self

    def onThirdCall(self):
        self.oncall = 3
        return self

    def returns(self, obj):
        def returnFunction(*args, **kwargs):
            return obj
        if self.args or self.kwargs or self.oncall:
            self._appendCondition(returnFunction)
            super(SinonStub, self).addWrapStub(self.stubfunc, self.condition)
        else:
            super(SinonStub, self).addWrapStub(returnFunction)
        return self

    def throws(self, exceptions=Exception):
        def exceptionFunction(*args, **kwargs):
            raise exceptions
        if self.args or self.kwargs or self.oncall:
            self._appendCondition(exceptionFunction)
            super(SinonStub, self).addWrapStub(self.stubfunc, self.condition)
        else:
            super(SinonStub, self).addWrapStub(exceptionFunction)
        return self
