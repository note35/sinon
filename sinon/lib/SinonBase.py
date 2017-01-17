'''
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE

sinon_base is the base of sinon_spy, it has three the major tasks
(1) when adding new spy/stub, it will determine the constructor of spy is valid or not
(2) when adding new spy/stub, it will wrap the it
(3) when deleting spy, it will help to make it self-destruction by using weakref queue
'''
import weakref
from copy import deepcopy
from types import FunctionType
from .util import ErrorHandler, Wrapper, TypeHandler

CPSCOPE = None

def init(scope):
    """
    Copy all values of scope into the class SinonGlobals
    Args:
        scope (eg. locals() or globals())
    Return:
        SinonGlobals instance
    """
    class SinonGlobals(object): #pylint: disable=too-few-public-methods
        """
        A fully empty class
        External can push the whole `scope` into this class through global function init()
        """
        pass

    global CPSCOPE #pylint: disable=global-statement
    CPSCOPE = SinonGlobals()
    funcs = [obj for obj in scope.values() if isinstance(obj, FunctionType)]
    for func in funcs:
        setattr(CPSCOPE, func.__name__, func)
    return CPSCOPE


class SinonBase(object):
    """
    A base class of any inspector such as spy/stub/expectation
    Generally, external will not use this directly
    because it does NOT provide any useful external function
    """

    class Pure(object): #pylint: disable=too-few-public-methods
        """
        A fully empty class with a func variable
        Pure class will make a function as a class/module
        """
        func = None

    _queue = [] # class-level variables for storing any inspector

    def __new__(cls, obj=None, prop=None, func=None):
        """
        Constructor of SinonBase
        It will new true base but return a proxy of weakref and store it in _queue
        Args:
            obj: None / function / instance method / module / class
                Inspected target
            prop: None / string
                Inspected target when obj contains callable things
            func: function / instance method
                ONLY used by stub, it will replace original target
        Return:
            weakref
        """
        new = super(SinonBase, cls).__new__(cls)
        if func:
            new.__init__(obj, prop, func)
        else:
            new.__init__(obj, prop)
        cls._queue.append(new)
        return weakref.proxy(new)

    def restore(self):
        """
        It will remove the wrapper of each inspector and remove weakref in _queue
        """
        self.unwrap()
        self._queue.remove(self)

    def __init__(self, obj=None, prop=None):
        """
        It will create the true base
        flow:
            __new__ => __init__
            => set type based on arguments
            => check the arguments is valid or not based on type
            => wrap the target
        Args:
            obj: None / function / instance method / module / class
                Inspected target
                If the target is None, it will create a Pure() class
            prop: None / string
                Inspected target when obj contains callable things
        """
        if not hasattr(self, "args_type"):
            self.__set_type(obj, prop)
            self.obj, self.prop = obj, prop
            self.__check_lock()
            self.wrap2spy()
            self.pure_count = 0
            self.is_in_queue = False

    def __call__(self, *args, **kwargs):
        """
        Customized __call__ function for two purpose
        If base is a Pure instance: call Pure.func
            Keeping original function works
            Wrapped function will record itself when is called
        If base is other type:
            Store called record
        Args:
            no limitation, only pure.func will use args
        Return:
            no limitation, only pure.func will return values
        """
        self.pure_count = self.pure_count + 1
        if self.args_type == "PURE":
            getattr(self.pure, "func")(*args, **kwargs)

    def __set_type(self, obj, prop):
        """
        Triage type based on arguments
        Here are four types of base: PURE, MODULE, MODULE_FUNCTION, FUNCTION
        Args:
            obj: None, FunctionType, ModuleType, Class, Instance
            prop: None, string
        """
        if TypeHandler.is_pure(obj, prop):
            self.args_type = "PURE"
            self.pure = SinonBase.Pure()
            setattr(self.pure, "func", Wrapper.empty_function)
            self.orig_func = None
        elif TypeHandler.is_module_function(obj, prop):
            self.args_type = "MODULE_FUNCTION"
            self.orig_func = None
        elif TypeHandler.is_function(obj):
            self.args_type = "FUNCTION"
            self.orig_func = None
        elif TypeHandler.is_module(obj):
            self.args_type = "MODULE"
        elif TypeHandler.is_instance(obj):
            obj = obj.__class__
            self.args_type = "MODULE"

    def __check_lock(self):
        """
        Cheking whether the inspector is wrapped or not
        (1) MODULE_FUNCTION: Check whether both obj/prop has __SINONLOCK__/LOCK or not
        (2) MODULE:          Check whether obj has __SINONLOCK__ or not
        (3) FUNCTION:        Check whether function(mock as a class) has LOCK or not
        Raise:
            lock_error: when inspector has been wrapped
        """
        if self.args_type == "MODULE_FUNCTION":
            if hasattr(getattr(self.obj, self.prop), "LOCK"):
                ErrorHandler.lock_error(self.prop)
        elif self.args_type == "MODULE":
            if hasattr(self.obj, "__SINONLOCK__"):
                ErrorHandler.lock_error(self.obj)
        elif self.args_type == "FUNCTION":
            if hasattr(getattr(CPSCOPE, self.obj.__name__), "LOCK"):
                ErrorHandler.lock_error(self.obj)

    def wrap2spy(self):
        """
        Wrapping the inspector as a spy based on the type
        """
        if self.args_type == "MODULE_FUNCTION":
            self.orig_func = deepcopy(getattr(self.obj, self.prop))
            setattr(self.obj, self.prop, Wrapper.wrapspy(getattr(self.obj, self.prop)))
        elif self.args_type == "MODULE":
            setattr(self.obj, "__SINONLOCK__", True)
        elif self.args_type == "FUNCTION":
            self.orig_func = deepcopy(getattr(CPSCOPE, self.obj.__name__))
            setattr(CPSCOPE, self.obj.__name__,
                    Wrapper.wrapspy(getattr(CPSCOPE, self.obj.__name__)))
        elif self.args_type == "PURE":
            self.orig_func = deepcopy(getattr(self.pure, "func"))
            setattr(self.pure, "func", Wrapper.wrapspy(getattr(self.pure, "func")))

    def unwrap(self):
        """
        Unwrapping the inspector based on the type
        """
        if self.args_type == "MODULE_FUNCTION":
            Wrapper.CALLQUEUE = [f for f in Wrapper.CALLQUEUE if f != getattr(self.obj, self.prop)]
            setattr(self.obj, self.prop, self.orig_func)
        elif self.args_type == "MODULE":
            Wrapper.CALLQUEUE = [f for f in Wrapper.CALLQUEUE if f != self]
            delattr(self.obj, "__SINONLOCK__")
        elif self.args_type == "FUNCTION":
            Wrapper.CALLQUEUE = [f for f in Wrapper.CALLQUEUE if f != getattr(CPSCOPE, self.obj.__name__)] #pylint: disable=line-too-long
            setattr(CPSCOPE, self.obj.__name__, self.orig_func)
        elif self.args_type == "PURE":
            Wrapper.CALLQUEUE = [f for f in Wrapper.CALLQUEUE if f != getattr(self.pure, "func")]
            setattr(self.pure, "func", self.orig_func)

    def wrap2stub(self, customfunc, condition=None):
        """
        Wrapping the inspector as a stub based on the type
        Args:
            customfunc: function
            condition: dict
        """
        if self.args_type == "MODULE_FUNCTION":
            setattr(self.obj, self.prop,
                    Wrapper.wrapspy(getattr(self.obj, self.prop), customfunc, condition))
        elif self.args_type == "MODULE":
            setattr(CPSCOPE, self.obj.__name__, Wrapper.EmptyClass)
        elif self.args_type == "FUNCTION":
            setattr(CPSCOPE, self.obj.__name__,
                    Wrapper.wrapspy(getattr(CPSCOPE, self.obj.__name__), customfunc, condition))
        elif self.args_type == "PURE":
            setattr(self.pure, "func",
                    Wrapper.wrapspy(getattr(self.pure, "func"), customfunc, condition))

    @classmethod
    def getCall(cls, n): #pylint: disable=invalid-name
        """
        Args:
            n: number (index of queue)
        Return:
            inspector of certain called
        Raise:
            get_callqueue_index_error if n is not valid index of queue
        """
        try:
            return cls._queue[n]
        except IndexError:
            ErrorHandler.get_callqueue_index_error(len(cls._queue))

    @property
    def g(self): #pylint: disable=invalid-name
        """
        Return:
            SinonGlobals instance
        """
        return CPSCOPE
