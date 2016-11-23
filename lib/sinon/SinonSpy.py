import sys
sys.path.insert(0, '../')

from lib.sinon.util import ErrorHandler, Wrapper, CollectionHandler
from lib.sinon.SinonBase import SinonBase

class SinonSpy(SinonBase):

    def __init__(self, obj=None, prop=None):
        super(SinonSpy, self).__init__(obj, prop)

    def restore(self):
        super(SinonSpy, self).restore()

    def addWrap(self):
        super(SinonSpy, self).addWrap()

    def delWrap(self):
        super(SinonSpy, self).delWrap()

    def __call__(self):
        super(SinonSpy, self).__call__()

    @property
    def args(self):
        if super(SinonSpy, self).args_type == "MODULE_FUNCTION":
            return getattr(super(SinonSpy, self).obj, super(SinonSpy, self).prop).args_list[-1]
        elif super(SinonSpy, self).args_type == "MODULE":
            pass
        elif super(SinonSpy, self).args_type == "FUNCTION":
            return getattr(g, super(SinonSpy, self).obj.__name__).args_list[-1]
        elif super(SinonSpy, self).args_type == "PURE":
            pass

    @property
    def kwargs(self):
        if super(SinonSpy, self).args_type == "MODULE_FUNCTION":
            return getattr(super(SinonSpy, self).obj, super(SinonSpy, self).prop).kwargs_list[-1]
        elif super(SinonSpy, self).args_type == "MODULE":
            pass
        elif super(SinonSpy, self).args_type == "FUNCTION":
            return getattr(g, super(SinonSpy, self).obj.__name__).kwargs_list[-1]
        elif super(SinonSpy, self).args_type == "PURE":
            pass

    @property
    def called(self):
        return True if super(SinonSpy, self).callCount > 0 else False

    @property
    def calledOnce(self):
        return True if super(SinonSpy, self).callCount == 1 else False

    @property
    def calledTwice(self):
        return True if super(SinonSpy, self).callCount == 2 else False

    @property
    def calledThrice(self):
        return True if super(SinonSpy, self).callCount == 3 else False

    @property
    def firstCall(self):
        return True if 0 in super(SinonSpy, self)._getCallQueueIndex() else False

    @property
    def secondCall(self):
        return True if 1 in super(SinonSpy, self)._getCallQueueIndex() else False

    @property
    def thirdCall(self):
        return True if 2 in super(SinonSpy, self)._getCallQueueIndex() else False

    @property
    def lastCall(self):
        return True if len(Wrapper.CALLQUEUE)-1 in super(SinonSpy, self)._getCallQueueIndex() else False

    def calledBefore(self, another_obj):
        if Wrapper.CALLQUEUE:
            return True if min(super(SinonSpy, self)._getCallQueueIndex()) < max(another_obj._getCallQueueIndex()) else False
        else:
            return False

    def calledAfter(self, another_obj):
        if Wrapper.CALLQUEUE:
            return True if max(super(SinonSpy, self)._getCallQueueIndex()) > min(another_obj._getCallQueueIndex()) else False
        else:
            return False

    def calledOn(obj):
        pass

    def alwaysCalledOn(obj):
        pass

    def calledWith(self, *args, **kwargs):
        if args and kwargs:
            return True if CollectionHandler.partialTupleInTupleList(super(SinonSpy, self)._args_list(), args) and CollectionHandler.partialDictInDictList(super(SinonSpy, self)._kwargs_list(), kwargs) else False
        elif args:
            return True if CollectionHandler.partialTupleInTupleList(super(SinonSpy, self)._args_list(), args) else False
        elif kwargs:
            return True if CollectionHandler.partialDictInDictList(super(SinonSpy, self)._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.calledWithEmptyError()

    def alwaysCalledWith(self, *args, **kwargs):
        if args and kwargs:
            return True if CollectionHandler.partialTupleInTupleListAlways(super(SinonSpy, self)._args_list(), args) and CollectionHandler.partialDictInDictListAlways(super(SinonSpy, self)._kwargs_list(), kwargs) else False
        elif args:
            return True if CollectionHandler.partialTupleInTupleListAlways(super(SinonSpy, self)._args_list(), args) else False
        elif kwargs:
            return True if CollectionHandler.partialDictInDictListAlways(super(SinonSpy, self)._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.calledWithEmptyError()

    def calledWithExactly(self, *args, **kwargs):
        if args and kwargs:
            return True if CollectionHandler.tupleInTupleList(super(SinonSpy, self)._args_list(), args) and CollectionHandler.dictInDictList(super(SinonSpy, self)._kwargs_list(), kwargs) else False
        elif args:
            return True if CollectionHandler.tupleInTupleList(super(SinonSpy, self)._args_list(), args) else False
        elif kwargs:
            return True if CollectionHandler.dictInDictList(super(SinonSpy, self)._kwargs_list(), kwargs) else False
        else:
            ErrorHandler.calledWithEmptyError()

    def alwaysCalledWithExactly(self, *args, **kwargs):
        if args and kwargs:
            return True if CollectionHandler.tupleInTupleListAlways(super(SinonSpy, self)._args_list(), args) and CollectionHandler.dictInDictListAlways(super(SinonSpy, self)._kwargs_list(), kwargs) else False
        elif args:
            return True if CollectionHandler.tupleInTupleListAlways(super(SinonSpy, self)._args_list(), args) else False
        elif kwargs:
            return True if CollectionHandler.dictInDictListAlways(super(SinonSpy, self)._kwargs_list(), kwargs) else False
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
            return True if len(super(SinonSpy, self)._error_list())>0 else False
        else:
            return CollectionHandler.objInList(super(SinonSpy, self)._error_list(), error_type)

    def alwaysThrew(self, error_type=None):
        if not error_type:
            return True if len(super(SinonSpy, self)._error_list()) == super(SinonSpy, self).callCount else False
        else:
            return CollectionHandler.objInListAlways(super(SinonSpy, self)._error_list(), error_type)

    def returned(self, obj):
        return CollectionHandler.objInList(super(SinonSpy, self)._ret_list(), obj)

    def alwaysReturned(self, obj):
        return CollectionHandler.objInListAlways(super(SinonSpy, self)._ret_list(), obj)

    @classmethod
    def getCall(self, n):
        try:
            return super(SinonSpy, self)._queue[n]
        except IndexError:
            ErrorHandler.getCallIndexError(len(super(SinonSpy, self)._queue))

    def thisValues(self):
        pass

    @property
    def args(self):
        return super(SinonSpy, self)._args_list()

    @property
    def kwargs(self):
        return super(SinonSpy, self)._kwargs_list()

    @property
    def exceptions(self):
        return super(SinonSpy, self)._error_list()

    @property
    def returnValues(self):
        return super(SinonSpy, self)._ret_list()

    def reset(self):
        super(SinonSpy, self).delWrap()
        super(SinonSpy, self).addWrap()
