def addStates(f):

    def empty_function(*args, **kwargs):
        pass

    def wrapped(*args, **kwargs):
        wrapped.callCount += 1
        if args:
            wrapped.args_list.append(args)
        if kwargs:
            wrapped.kwargs_list.append(kwargs)
        try:
            return f(*args, **kwargs)
        except:
            wrapped.error_list.append(Exception)
            return empty_function
           
    wrapped.callCount = 0
    wrapped.args_list = []
    wrapped.kwargs_list = []
    wrapped.error_list = []

    return wrapped


def wrap(f):

    @addStates
    def fn(*args, **kwargs):
        return f(*args, **kwargs)

    return fn
