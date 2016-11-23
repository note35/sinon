import sys
sys.path.insert(0, '../')

from lib.sinon.util import ErrorHandler, Wrapper, CollectionHandler
from lib.sinon.SinonBase import SinonBase

class SinonSpy(SinonBase):

    @property
    def args(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).args_list[-1]
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(g, self.obj.__name__).args_list[-1]
        elif self.args_type == "PURE":
            pass

    @property
    def kwargs(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).kwargs_list[-1]
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(g, self.obj.__name__).kwargs_list[-1]
        elif self.args_type == "PURE":
            pass

    @property
    def called(self):
        return True if self.callCount > 0 else False

    @property
    def calledOnce(self):
        return True if self.callCount == 1 else False

    @property
    def calledTwice(self):
        return True if self.callCount == 2 else False

    @property
    def calledThrice(self):
        return True if self.callCount == 3 else False

    @property
    def firstCall(self):
        return True if 0 in self._getCallQueueIndex() else False

    @property
    def secondCall(self):
        return True if 1 in self._getCallQueueIndex() else False

    @property
    def thirdCall(self):
        return True if 2 in self._getCallQueueIndex() else False

    @property
    def lastCall(self):
        return True if len(Wrapper.CALLQUEUE)-1 in self._getCallQueueIndex() else False

    def calledBefore(self, another_obj):
        if Wrapper.CALLQUEUE:
            return True if min(self._getCallQueueIndex()) < max(another_obj._getCallQueueIndex()) else False
        else:
            return False

    def calledAfter(self, another_obj):
        if Wrapper.CALLQUEUE:
            return True if max(self._getCallQueueIndex()) > min(another_obj._getCallQueueIndex()) else False
        else:
            return False

    def calledOn(obj):
        pass

    def alwaysCalledOn(obj):
        pass

    def calledWith(self, *args, **kwargs):
        if args and kwargs:
            return True if CollectionHandler.partialTupleInTupleList(self._args_list(), args) and CollectionHandler.partialDictInDictList(self._kwargs_list(), kwargs) else False
        elif args:
            return True if CollectionHandler.partialTupleInTupleList(self._args_list(), args) else False
        elif kwargs:
            return True if CollectionHandler.partialDictInDictList(self._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.calledWithEmptyError()

    def alwaysCalledWith(self, *args, **kwargs):
        if args and kwargs:
            return True if CollectionHandler.partialTupleInTupleListAlways(self._args_list(), args) and CollectionHandler.partialDictInDictListAlways(self._kwargs_list(), kwargs) else False
        elif args:
            return True if CollectionHandler.partialTupleInTupleListAlways(self._args_list(), args) else False
        elif kwargs:
            return True if CollectionHandler.partialDictInDictListAlways(self._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.calledWithEmptyError()

    def calledWithExactly(self, *args, **kwargs):
        if args and kwargs:
            return True if CollectionHandler.tupleInTupleList(self._args_list(), args) and CollectionHandler.dictInDictList(self._kwargs_list(), kwargs) else False
        elif args:
            return True if CollectionHandler.tupleInTupleList(self._args_list(), args) else False
        elif kwargs:
            return True if CollectionHandler.dictInDictList(self._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.calledWithEmptyError()

    def alwaysCalledWithExactly(self, *args, **kwargs):
        if args and kwargs:
            return True if CollectionHandler.tupleInTupleListAlways(self._args_list(), args) and CollectionHandler.dictInDictListAlways(self._kwargs_list(), kwargs) else False
        elif args:
            return True if CollectionHandler.tupleInTupleListAlways(self._args_list(), args) else False
        elif kwargs:
            return True if CollectionHandler.dictInDictListAlways(self._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.calledWithEmptyError()

    def calledWithMatch(self, *args, **kwargs):
        pass

    def alwaysCalledWithMatch(self, *args, **kwargs):
        pass

    def calledWithNew():
        pass

    def neverCalledWith(self, *args, **kwargs):
        return not self.calledWith(*args, **kwargs)

    def neverCalledWithMatch(self, *args, **kwargs):
        pass

    def threw(self, error_type=None):
        if not error_type:
            return True if len(self._error_list())>0 else False
        else:
            return CollectionHandler.objInList(self._error_list(), error_type)

    def alwaysThrew(self, error_type=None):
        if not error_type:
            return True if len(self._error_list()) == self.callCount else False
        else:
            return CollectionHandler.objInListAlways(self._error_list(), error_type)

    def returned(self, obj):
        return CollectionHandler.objInList(self._ret_list(), obj)

    def alwaysReturned(self, obj):
        return CollectionHandler.objInListAlways(self._ret_list(), obj)

    @classmethod
    def getCall(self, n):
        try:
            return self._queue[n]
        except IndexError:
            ErrorHandler.getCallIndexError(len(self._queue))

    def thisValues(self):
        pass

    @property
    def args(self):
        return self._args_list()

    @property
    def kwargs(self):
        return self._kwargs_list()

    @property
    def exceptions(self):
        return self._error_list()

    @property
    def returnValues(self):
        return self._ret_list()

    def reset(self):
        self.delWrap()
        self.addWrap()
