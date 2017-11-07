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

def wrapspy(func, customfunc=None, conditions=None): #pylint: disable=missing-docstring
    if customfunc:
        @__add_spy
        def wrapped_fn(*args, **kwargs):
            """
            A wrapped stub function
            """
            return __gen_stub_func(customfunc, conditions, wrapped_fn, *args, **kwargs)
    else:
        @__add_spy
        def wrapped_fn(*args, **kwargs):
            """
            A wrapped spy function
            """
            return func(*args, **kwargs)
    return wrapped_fn

def __add_spy(func):
    def __set__(value, new_list):
        """
        For python 2.x compatibility
        """
        setattr(wrapped, value, new_list)

    def wrapped(*args, **kwargs):
        """
        Fully manipulatable inspector function
        """
        wrapped.callCount += 1
        wrapped.args_list.append(args)
        wrapped.kwargs_list.append(kwargs)

        call = SpyCall()
        call.args = args
        call.kwargs = kwargs
        call.stack = traceback.format_stack()
        wrapped.call_list.append(call)

        try:
            ret = func(*args, **kwargs)
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

def __gen_index_list(conditions, *args, **kwargs):
    """
    Args:
        conditions: dictionary, the SinonStub's conditions (the user-defined behaviour for the stub)
        args: tuple, the arguments inputed by the user
        kwargs: dictionary, the keyword arguments inputed by the user
    Returns:
        list, the list of indices in conditions for which the user args/kwargs match
    """
    return __get_call_indices(conditions["target"], args, kwargs, conditions["args"], conditions["kwargs"])

def __get_call_indices(target, args, kwargs, args_list, kwargs_list):
    """
    Args:
        target: object, the callback (self) argument for the owner of the stubbed function
        args: tuple, the arguments inputed by the user
        kwargs: dictionary, the keyword arguments inputed by the user
        args_list: list, a list of argument tuples
        kwargs_list: list, a list of keyword argument dictionaries
    Returns:
        list, the list of indices in args_list/kwargs_list for which the user args/kwargs match
    """
    # Todo: dirty hack
    if len(args) > 0:
        if target == args[0].__class__:
            # Note: ignore args[0] because it is a callback (self) in this condition combination
            args = args[1:]
            args_list = [i[1:] if i and i[0].__class__ == target else i for i in args_list]

    if args and kwargs:
        if args in args_list and kwargs in kwargs_list:
            args_indices = [i for i, x in enumerate(args_list) if x == args]
            kwargs_indices = [i for i, x in enumerate(kwargs_list) if x == kwargs]
            return list(set(args_indices).intersection(kwargs_indices))
    # args only
    elif args:
        if args in args_list:
            return [i for i, x in enumerate(args_list) if x == args and not kwargs_list[i]]
    #kwargs only
    elif kwargs:
        if kwargs in kwargs_list:
            return [i for i, x in enumerate(kwargs_list) if x == kwargs and not args_list[i]]
    else:
        return []

def __get_call_count(target, args, kwargs, args_list, kwargs_list):
    """
    Args:
        target: object, the callback (self) argument for the owner of the stubbed function
        args: tuple, the arguments inputed by the user
        kwargs: dictionary, the keyword arguments inputed by the user
        args_list: list, the tuples of args from all the times this stub was called
        kwargs_list: list, the dictionaries of kwargs from all the times this stub was called
    Returns:
        integer, the number of times this combination of args/kwargs has been called
    """
    return len(__get_call_indices(target, args, kwargs, args_list, kwargs_list))

def __gen_retfunc_with_args(index_list, conditions, func, *args, **kwargs):
    """
    Pre-conditions:
       (1) The user has created a stub and specified the stub behaviour ("conditions")
       (2) The user has called the stub function ("func") with the specified "args" and "kwargs"
       (3) One or more 'withArgs' conditions were applicable in this case
    Args:
        index_list: list, the list of indices in conditions for which the user args/kwargs match
        conditions: dictionary, the SinonStub's conditions (the user-defined behaviour for the stub)
        func: function, the SinonStub function wrapper (as defined by calls to returns/throws)
        args: tuple, the arguments inputed by the user
        kwargs: dictionary, the keyword arguments inputed by the user
    Returns:
        any type, the appropriate return value, based on the stub's behaviour setup and the user input
    """
    # indices with an arg and oncall have higher priority and should be checked first
    indices_with_oncall = [i for i in reversed(index_list) if conditions["oncall"][i]]
    # if there are any combined withArgs+onCall conditions
    if indices_with_oncall:
        call_count = __get_call_count(conditions["target"], args, kwargs, func.args_list, func.kwargs_list)
        for i in indices_with_oncall:
            if conditions["oncall"][i] == call_count:
                return conditions["action"][i](*args, **kwargs)
    # else if there are simple withArgs conditions
    indices_without_oncall = [i for i in reversed(index_list) if not conditions["oncall"][i]]
    if indices_without_oncall:
        max_index = max(indices_without_oncall)
        return conditions["action"][max_index](*args, **kwargs)
    # else all conditions did not match
    return conditions["default"](*args, **kwargs)

def __gen_retfunc_without_args(conditions, func, *args, **kwargs):
    """
    Pre-conditions:
       (1) The user has created a stub and specified the stub behaviour ("conditions")
       (2) The user has called the stub function ("func") with the specified "args" and "kwargs"
       (3) No 'withArgs' conditions were applicable in this case
    Args:
        conditions: dictionary, the SinonStub's conditions (the user-defined behaviour for the stub)
        func: function, the SinonStub function wrapper (as defined by calls to returns/throws)
        args: tuple, the arguments inputed by the user
        kwargs: dictionary, the keyword arguments inputed by the user
    Returns:
        any type, the appropriate return value, based on the stub's behaviour setup and the user input
    """
    # if there might be applicable onCall conditions
    if func.callCount in conditions["oncall"]:
        index_list = [i for i, x in enumerate(conditions["oncall"]) if x and not conditions["args"][i] and not conditions["kwargs"][i]]
        for i in reversed(index_list):
            # if the onCall condition applies
            if func.callCount == conditions["oncall"][i]:
                return conditions["action"][i](*args, **kwargs)
    # else all conditions did not match
    return conditions["default"](*args, **kwargs)

def __gen_stub_func(customfunc, conditions, func, *args, **kwargs):
    """
    Args:
        customfunc: function, the user's custom function with which they want to replace the original
        conditions: dictionary, the SinonStub's conditions (the user-defined behaviour for the stub)
        func: function, the SinonStub function wrapper (as defined by calls to returns/throws)
        args: tuple, the arguments inputed by the user
        kwargs: dictionary, the keyword arguments inputed by the user
    Returns:
        any type, the appropriate return value, based on the stub's behaviour setup and the user input
    """
    # if the user defined stub behavioural conditions
    if conditions:
        index_list = __gen_index_list(conditions, *args, **kwargs)
        # if there are 'withArgs' conditions that might be applicable
        if index_list:
            return __gen_retfunc_with_args(index_list, conditions, func, *args, **kwargs)
        # else no 'withArgs' conditions are applicable
        else:
            return __gen_retfunc_without_args(conditions, func, *args, **kwargs)
    # else there are no behavioural conditions
    else:
        return customfunc(*args, **kwargs)
