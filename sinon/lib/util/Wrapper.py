"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
"""
global CALLQUEUE #pylint: disable=global-at-module-level
CALLQUEUE = []


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

def wrapspy(func, customfunc=None, condition=None): #pylint: disable=missing-docstring
    if customfunc:
        @__add_spy
        def wrapped_fn(*args, **kwargs):
            """
            A wrapped stub function
            """
            return __gen_stub_func(customfunc, condition, wrapped_fn, *args, **kwargs)
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
        CALLQUEUE.append(wrapped)
        if args:
            wrapped.args_list.append(args)
        if kwargs:
            wrapped.kwargs_list.append(kwargs)
        try:
            wrapped.ret_list.append(func(*args, **kwargs))
            return func(*args, **kwargs)
        except Exception as excpt:
            # Todo: make sure e.__class__ is enough for all purpose or not
            wrapped.error_list.append(excpt.__class__)
            return func(*args, **kwargs)
    wrapped.__set__ = __set__
    wrapped.callCount = 0
    wrapped.args_list = []
    wrapped.kwargs_list = []
    wrapped.error_list = []
    wrapped.ret_list = []
    wrapped.LOCK = True
    return wrapped

def __gen_index_list(condition, *args, **kwargs):
    # Generating index list based on arguments and condition
    # Note: ignore args[0] because it is callback in this condition
    # combination
    if args[1:] and kwargs:
        if args[1:] in condition["args"] and kwargs in condition["kwargs"]:
            args_indices = [i for i, x in enumerate(condition["args"]) if x == args[1:]]
            kwargs_indices = [i for i, x in enumerate(condition["kwargs"]) if x == kwargs]
            return list(set(args_indices).intersection(kwargs_indices))
    # args only
    elif args[1:]:
        if args[1:] in condition["args"]:
            return [i for i, x in enumerate(condition["args"]) if x == args[1:] and not condition["kwargs"][i]]
    #kwargs only
    elif kwargs:
        if kwargs in condition["kwargs"]:
            return [i for i, x in enumerate(condition["kwargs"]) if x == kwargs and not condition["args"][i]]

def __gen_retfunc_with_args(index_list, condition, func, *args, **kwargs):
    """
    @return customfunc by condition(args/kwargs || args+oncall/kwargs+oncall)
    """
    for i in reversed(index_list):
        if not condition["oncall"][i] or condition["oncall"][i] == func.callCount:
            return condition["action"][i](*args, **kwargs)

def __gen_retfunc_without_args(index_list, condition, func, *args, **kwargs):
    """
    @return customfunc by condition(oncall)
    """
    if func.callCount in condition["oncall"]:
        index_list = [i for i, x in enumerate(condition["oncall"]) if x and not condition["args"][i] and not condition["kwargs"][i]]
        for i in reversed(index_list):
            if func.callCount == condition["oncall"][i]:
                return condition["action"][i](*args, **kwargs)

def __gen_stub_func(customfunc, condition, func, *args, **kwargs):
    if condition:
        index_list = __gen_index_list(condition, *args, **kwargs)
        if index_list:
            return __gen_retfunc_with_args(index_list, condition, func, *args, **kwargs)
        return __gen_retfunc_without_args(index_list, condition, func, *args, **kwargs)
    #return stub function
    return customfunc(*args, **kwargs)
