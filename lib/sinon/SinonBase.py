import sys
sys.path.insert(0, '../')

import weakref
import inspect
from copy import deepcopy
from types import ModuleType, FunctionType

from lib.sinon.util import ErrorHandler, Wrapper

global LOCK
LOCK = "__SINONLOCK__"

class SinonGlobals(object):
    pass

def init(target_globals):
    global g
    g = SinonGlobals()
    funcs = [obj for obj in target_globals.values() if isinstance(obj, FunctionType)]
    for func in funcs:
        setattr(g, func.__name__, func)

class SinonBase(object):

    _queue = []

    def __new__(self, obj=None, prop=None):
        new = super(SinonBase, self).__new__(self)
        new.__init__(obj, prop)
        self._queue.append(new)
        return weakref.proxy(new)

    
    def restore(self):
        self.delWrap()
        self._queue.remove(self)


    def __init__(self, obj=None, prop=None):

        if not hasattr(self, "args_type"):
            self.setType(obj, prop)
            self.obj, self.prop = obj, prop
            self.checkLock()
            self.addWrap()
            self.pure_count = 0


    def setType(self, obj, prop):
        # pure
        if not prop and not obj:
            self.args_type = "PURE"

        # object
        if obj and (isinstance(obj, ModuleType) or inspect.isclass(obj) or isinstance(obj, FunctionType)):
            if isinstance(obj, ModuleType) or inspect.isclass(obj):
                self.args_type = "MODULE"
            elif isinstance(obj, FunctionType):
                self.args_type = "FUNCTION"
                self.orig_func = None
        elif obj:
            ErrorHandler.objTypeError(obj) 

        # property
        if prop and (isinstance(prop, str) or isinstance(prop, unicode)):
            if prop in dir(obj):
                self.args_type = "MODULE_FUNCTION"
                self.orig_func = None
            else:
                ErrorHandler.propInObjError(obj, prop)
        elif prop:
            ErrorHandler.propTypeError(prop)


    def checkLock(self):
        if self.args_type == "MODULE_FUNCTION":
            if hasattr(self.obj, LOCK):
                ErrorHandler.lockError(self.obj.__name__)
            if hasattr(getattr(self.obj, self.prop), "callCount"):
                ErrorHandler.lockError(self.prop)
        elif self.args_type == "MODULE":
            if hasattr(self.obj, LOCK):
                ErrorHandler.lockError(self.obj.__name__)
        elif self.args_type == "FUNCTION":
            if hasattr(getattr(g, self.obj.__name__), "callCount"):
                ErrorHandler.lockError(self.obj.__name__)
        elif self.args_type == "PURE":
            pass


    def addWrap(self):
        if self.args_type == "MODULE_FUNCTION":
            self.orig_func = deepcopy(getattr(self.obj, self.prop))
            setattr(self.obj, self.prop, Wrapper.wrap(getattr(self.obj, self.prop)))
        elif self.args_type == "MODULE":
            setattr(self.obj, LOCK, True)
            #for key, value in self.obj.__dict__.items():
            #   if hasattr(value, '__call__'):
            #       setattr(self.obj, key, Wrapper.wrap(value))
        elif self.args_type == "FUNCTION":
            self.orig_func = deepcopy(getattr(g, self.obj.__name__))
            setattr(g, self.obj.__name__, Wrapper.wrap(getattr(g, self.obj.__name__)))
        elif self.args_type == "PURE":
            pass


    def delWrap(self):
        if self.args_type == "MODULE_FUNCTION":
            setattr(self.obj, self.prop, self.orig_func)
        elif self.args_type == "MODULE":
            delattr(self.obj, LOCK)
        elif self.args_type == "FUNCTION":
            setattr(g, self.obj.__name__, self.orig_func)
        elif self.args_type == "PURE":
            pass


    def __call__(self):
        self.pure_count = self.pure_count + 1
 

    @property
    def callCount(self):
        if self.args_type == "MODULE_FUNCTION":
            return getattr(self.obj, self.prop).callCount
        elif self.args_type == "MODULE":
            return self.pure_count
        elif self.args_type == "FUNCTION":
            return getattr(g, self.obj.__name__).callCount
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
    def calledTrice(self):
        return True if self.callCount == 3 else False

    @property
    def firstCall(self):
        return True if self._queue.index(self) == 0 else False

    @property
    def secondCall(self):
        return True if self._queue.index(self) == 1 else False

    @property
    def thirdCall(self):
        return True if self._queue.index(self) == 2 else False

    @property
    def lastCall(self):
        return True if len(self._queue) - self._queue.index(self) - 1 == 0 else False

    def calledBefore(self, another_obj):
        return True if self._queue.index(self) < self._queue.index(another_obj) else False

    def calledAfter(self, another_obj):
        return True if self._queue.index(self) > self._queue.index(another_obj) else False

    def calledWith(self, *args):
        pass

    def threw(self):
        pass

    @property
    def args(self):
        if self.args_type == "METHOD":
            print(getattr(self.module, self.method).args)
        pass 

