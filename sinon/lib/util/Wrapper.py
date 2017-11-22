"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
"""
import traceback
import sys
from .SpyCall import SpyCall

class ClassPropertyDescriptor(object): #pylint: disable=too-few-public-methods
    """
    A standard classPropertyDescriptor
    This class is ONLY for internal wrapped function
    """
    def __init__(self, func):
        self.func = func
    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.func.__get__(obj, klass)()

def classproperty(func): #pylint: disable=missing-docstring
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)

class EmptyClass(object): #pylint: disable=too-few-public-methods,missing-docstring
    pass

def empty_function(*args, **kwargs): #pylint: disable=unused-argument,missing-docstring
    pass

def wrap_spy(function, owner=None):
    """
    Surrounds the given 'function' with a spy wrapper that tracks usage data, such as:
      * call count
      * arguments it was called with
      * keyword argument it was called with
      * return values
      * etc.

    Parameters:
        function: function, could be one of 3 things:
                    1. the original function the user wants to spy on
                    2. the custom function the user specified to replace the original
                    3. a default function configurable via returns/throws
        owner: object, the owner of the original function. It is necessary in certain cases
               to specify this, such as when the user stubs a class. Otherwise, the SpyCall
               arguments will erroneously include the 'owner' as the first parameter of every call.
    Returns:
        function, the spy wrapper that is replacing the inputted function
    """
    def __set__(value, new_list):
        """
        For python 2.x compatibility
        """
        setattr(wrapped, value, new_list)

    def wrapped(*args, **kwargs):
        """
        Fully manipulatable inspector function
        """
        if owner:
            if len(args) > 0:
                if owner == args[0].__class__:
                    args = args[1:]
        
        wrapped.callCount += 1
        wrapped.args_list.append(args)
        wrapped.kwargs_list.append(kwargs)

        call = SpyCall()
        call.args = args
        call.kwargs = kwargs
        call.stack = traceback.format_stack()
        wrapped.call_list.append(call)

        try:
            ret = function(*args, **kwargs)
            wrapped.ret_list.append(ret)
            call.returnValue = ret
            return ret
        except BaseException as excpt:
            # Todo: make sure e.__class__ is enough for all purpose or not
            wrapped.error_list.append(excpt.__class__)
            call.exception = excpt
            raise excpt

    wrapped.__set__ = __set__
    wrapped.callCount = 0
    wrapped.args_list = []
    wrapped.call_list = []
    wrapped.kwargs_list = []
    wrapped.error_list = []
    wrapped.ret_list = []
    wrapped.LOCK = True
    return wrapped
