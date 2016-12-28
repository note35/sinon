from .util import ErrorHandler, Wrapper, CollectionHandler
from .SinonBase import SinonBase
from .SinonMatcher import SinonMatcher, Matcher

class SinonSpy(SinonBase):

    def __init__(self, obj=None, prop=None):
        super(SinonSpy, self).__init__(obj, prop)
        self._dtArgs = self._dtArgsOn

    def _dtArgsOn(self, args):
        """
        inspect args as a duck type
        1. return itself       ,if it is a SinonMatcher
        2. return SinonMatcher ,if it is not a SinonMatcher
        """
        if not isinstance(args, Matcher):
            return SinonMatcher(args)
        else:
            return args

    def _dtArgsOff(self, args):
        return args

    def _args_list(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).args_list
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).args_list
        elif self.args_type == "PURE":
            return getattr(self.pure, "func").args_list

    def _kwargs_list(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).kwargs_list
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).kwargs_list
        elif self.args_type == "PURE":
            return getattr(self.pure, "func").kwargs_list

    def _error_list(self): 
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).error_list
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).error_list
        elif self.args_type == "PURE":
            return getattr(self.pure, "func").error_list

    def _ret_list(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).ret_list
        elif self.args_type == "MODULE":
            pass
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).ret_list
        elif self.args_type == "PURE":
            return getattr(self.pure, "func").ret_list

    def _getCallQueueIndex(self):
        if self.args_type == "MODULE_FUNCTION":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE) if val == getattr(self.obj, self.prop)]
        elif self.args_type == "MODULE":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE) if val == self]
        elif self.args_type == "FUNCTION":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE) if val == getattr(self.g, self.obj.__name__)]
        elif self.args_type == "PURE":
            return [idx for idx, val in enumerate(Wrapper.CALLQUEUE) if val == getattr(self.pure, "func")]

    @property
    def callCount(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).callCount
        elif self.args_type == "MODULE":
            return self.pure_count
        elif self.args_type == "FUNCTION":
            return getattr(self.g, self.obj.__name__).callCount
        elif self.args_type == "PURE":
            return self.pure_count

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
        if len(self._getCallQueueIndex()) == 0:
            ErrorHandler.CallQueueIsEmptyError() 
        if Wrapper.CALLQUEUE:
            return True if min(self._getCallQueueIndex()) < max(another_obj._getCallQueueIndex()) else False
        else:
            return False

    def calledAfter(self, another_obj):
        if len(self._getCallQueueIndex()) == 0:
            ErrorHandler.CallQueueIsEmptyError() 
        if Wrapper.CALLQUEUE:
            return True if max(self._getCallQueueIndex()) > min(another_obj._getCallQueueIndex()) else False
        else:
            return False

    #def calledOn(obj):
    #    pass

    #def alwaysCalledOn(obj):
    #    pass

    def calledWith(self, *args, **kwargs):
        self._dtArgs = self._dtArgsOff
        return self.calledWithMatch(*args, **kwargs)

    def alwaysCalledWith(self, *args, **kwargs):
        self._dtArgs = self._dtArgsOff
        return self.alwaysCalledWithMatch(*args, **kwargs)

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
        """
        Note: sinon.js have no definition of combination case, here is current implementation:

            for args or kwargs, it should be matched in each individual call
            eg. func(1,2,3) -> func(4,5,6)
                spy.calledWithMatch(1,5) is not valid
            eg. func(a=1,b=2,c=3) -> func(a=4,b=5,c=6)
                spy.calledWithMatch(a=1,b=5,c=6) is not valid

            however, for combination case, it should be matched separated
            eg. func(1,2,c=3) -> func(2,b=5,c=6)
                spy.calledWithMatch(1,2,c=3) is valid, because spy.calledWithMatch(1,2) and spy.calledWithMatch(c=3) is valid
                spy.calledWithMatch(1,c=6) is valid  , because spy.calledWithMatch(1)   and spy.calledWithMatch(c=6) is valid
                spy.calledWithMatch(1,2,c=6) is valid, because spy.calledWithMatch(1,2) and spy.calledWithMatch(c=6) is valid
        """
        if args and kwargs:
            return CollectionHandler.argsPartialCompare(args, self._args_list(), self._dtArgs) and CollectionHandler.kwargsPartialCompare(kwargs, self._kwargs_list(), self._dtArgs)
        elif args:
            return CollectionHandler.argsPartialCompare(args, self._args_list(), self._dtArgs)
        elif kwargs:
            return CollectionHandler.kwargsPartialCompare(kwargs, self._kwargs_list(), self._dtArgs)
        else:
            ErrorHandler.calledWithEmptyError()
        self._dtArgs = self._dtArgsOn

    def alwaysCalledWithMatch(self, *args, **kwargs):
        if args and kwargs:
            return CollectionHandler.argsPartialCompare(args, self._args_list(), self._dtArgs, always=True) and CollectionHandler.kwargsPartialCompare(kwargs, self._kwargs_list(), self._dtArgs, always=True)
        elif args:
            return CollectionHandler.argsPartialCompare(args, self._args_list(), self._dtArgs, always=True)
        elif kwargs:
            return CollectionHandler.kwargsPartialCompare(kwargs, self._kwargs_list(), self._dtArgs, always=True)
        else:
            ErrorHandler.calledWithEmptyError()
        self._dtArgs = self._dtArgsOn

    #def calledWithNew():
    #    pass

    def neverCalledWith(self, *args, **kwargs):
        return not self.calledWith(*args, **kwargs)

    def neverCalledWithMatch(self, *args, **kwargs):
        return not self.calledWithMatch(*args, **kwargs)

    def threw(self, error_type=None):
        if not error_type:
            return True if len(self._error_list())>0 else False
        else:
            return CollectionHandler.objInList(self._error_list(), error_type)

    def alwaysThrew(self, error_type=None):
        if self.callCount == 0:
            return False
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

    #def thisValues(self):
    #    pass

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
        super(SinonSpy, self).delWrapSpy()
        super(SinonSpy, self).addWrapSpy()
