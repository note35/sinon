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
            return emptyFunction
    wrapped.callCount = 0
    wrapped.args_list = []
    wrapped.kwargs_list = []
    wrapped.error_list = []
    wrapped.ret_list = []
    wrapped.LOCK = True
    return wrapped


def addStub(f):
    def wrapped(*args, **kwargs):
        wrapped.callCount += 1
        return f(*args, **kwargs)
    wrapped.callCount = 0
    wrapped.LOCK = True
    return wrapped


def wrapStub(f, customfunc, condition):
    if not customfunc:
        customfunc = emptyFunction
    @addStub
    def fn(*args, **kwargs):
        if condition:
            if args[1:] and kwargs:
                if args[1:] in condition["args"] and kwargs in condition["kwargs"]:
                    args_indices = [i for i, x in enumerate(condition["args"]) if x == args[1:]]
                    kwargs_indices = [i for i, x in enumerate(condition["kwargs"]) if x == kwargs]
                    index_list = (list(set(args_indices).intersection(kwargs_indices)))
                    for i in reversed(index_list):
                        if not condition["oncall"][i] or condition["oncall"][i] == fn.callCount:
                            return condition["action"][i](*args, **kwargs)
            elif args[1:]:
                if args[1:] in condition["args"]:
                    index_list = [i for i, x in enumerate(condition["args"]) if x == args[1:] and not condition["kwargs"][i]]
                    for i in reversed(index_list):
                        if not condition["oncall"][i] or condition["oncall"][i] == fn.callCount:
                            return condition["action"][i](*args, **kwargs)
            elif kwargs:
                if kwargs in condition["kwargs"]:
                    index_list = [i for i, x in enumerate(condition["kwargs"]) if x == kwargs and not condition["args"][i]]
                    for i in reversed(index_list):
                        if not condition["oncall"][i] or condition["oncall"][i] == fn.callCount:
                            return condition["action"][i](*args, **kwargs)
            elif fn.callCount in condition["oncall"]:
                index_list = [i for i, x in enumerate(condition["oncall"]) if x and not condition["args"][i] and not condition["kwargs"][i]]
                for i in reversed(index_list):
                    if fn.callCount == condition["oncall"][i]:
                        return condition["action"][i](*args, **kwargs)
        return customfunc(*args, **kwargs)
    return fn


def wrapSpy(f):
    @addSpy
    def fn(*args, **kwargs):
        return f(*args, **kwargs)
    return fn
