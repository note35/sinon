global CALLQUEUE
CALLQUEUE = []


class empty_class(object):
    pass


def empty_function(*args, **kwargs):
    pass


def addStates(f):
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
            return empty_function
    wrapped.callCount = 0
    wrapped.args_list = []
    wrapped.kwargs_list = []
    wrapped.error_list = []
    wrapped.ret_list = []
    wrapped.LOCK = True
    return wrapped


def addLock(f):
    def wrapped(*args, **kwargs):
        return f(*args, **kwargs)
    wrapped.LOCK = True
    return wrapped


def wrap_custom_func(f, custom_func=None):
    if not custom_func:
        custom_func = empty_function
    @addLock
    def fn(*args, **kwargs):
        return custom_func(*args, **kwargs)
    return fn


def wrap(f):
    @addStates
    def fn(*args, **kwargs):
        return f(*args, **kwargs)
    return fn
