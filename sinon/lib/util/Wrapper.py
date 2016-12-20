global CALLQUEUE
CALLQUEUE = []


class EmptyClass(object):
    pass


def emptyFunction(*args, **kwargs):
    pass


def addSpy(f):
    def wrapped(*args, **kwargs):
        wrapped.callCount += 1
        CALLQUEUE.append(wrapped)
        if args:
            wrapped.args_list.append(args)
        if kwargs:
            wrapped.kwargs_list.append(kwargs)
        try:
            wrapped.ret_list.append(f(*args, **kwargs))
            return f(*args, **kwargs)
        except Exception as e:
            # Todo: make sure e.__class__ is enough for all purpose or not
            wrapped.error_list.append(e.__class__)
            return f(*args, **kwargs)
    wrapped.callCount = 0
    wrapped.args_list = []
    wrapped.kwargs_list = []
    wrapped.error_list = []
    wrapped.ret_list = []
    wrapped.LOCK = True
    return wrapped
   

def _genIndexList(condition, *args, **kwargs): 
    # Generating index list based on arguments and condition
    # Note: ignore args[0] because it is callback in this condition
    # combination
    if args[1:] and kwargs:
        if args[1:] in condition["args"] and kwargs in condition["kwargs"]:
            args_indices = [i for i, x in enumerate(condition["args"]) if x == args[1:]]
            kwargs_indices = [i for i, x in enumerate(condition["kwargs"]) if x == kwargs]
            return (list(set(args_indices).intersection(kwargs_indices)))
    # args only
    elif args[1:]:
        if args[1:] in condition["args"]:
            return [i for i, x in enumerate(condition["args"]) if x == args[1:] and not condition["kwargs"][i]]
    #kwargs only
    elif kwargs:
        if kwargs in condition["kwargs"]:
            return [i for i, x in enumerate(condition["kwargs"]) if x == kwargs and not condition["args"][i]]


def _genRetFuncWithArgs(index_list, condition, fn, *args, **kwargs):
    """
    @return customfunc by condition(args/kwargs || args+oncall/kwargs+oncall)
    """
    for i in reversed(index_list):
        if not condition["oncall"][i] or condition["oncall"][i] == fn.callCount:
            return condition["action"][i](*args, **kwargs)


def _genRetFuncWithoutArgs(index_list, condition, fn, *args, **kwargs):
    """
    @return customfunc by condition(oncall)
    """
    if fn.callCount in condition["oncall"]:
        index_list = [i for i, x in enumerate(condition["oncall"]) if x and not condition["args"][i] and not condition["kwargs"][i]]
        for i in reversed(index_list):
            if fn.callCount == condition["oncall"][i]:
                return condition["action"][i](*args, **kwargs)


def _genStubFunc(customfunc, condition, fn, *args, **kwargs):
    if condition:
        index_list = _genIndexList(condition, *args, **kwargs)
        if index_list:
            return _genRetFuncWithArgs(index_list, condition, fn, *args, **kwargs)
        return _genRetFuncWithoutArgs(index_list, condition, fn, *args, **kwargs)
    #return stub function
    return customfunc(*args, **kwargs)


def wrapSpy(f, customfunc=None, condition=None):
    if customfunc:
        @addSpy
        def fn(*args, **kwargs):
            return _genStubFunc(customfunc, condition, fn, *args, **kwargs)
    else:
        @addSpy
        def fn(*args, **kwargs):
            return f(*args, **kwargs)
    return fn
