def addStates(f):
    def wrapped(*args, **kwargs):
        wrapped.callCount += 1
        if args:
            wrapped.args.append(args)
        if kwargs:
            wrapped.kwargs.append(kwargs)
        return f(*args, **kwargs)
    wrapped.callCount = 0
    wrapped.args = []
    wrapped.kwargs = []
    return wrapped

def wrap(f):
    @addStates
    def fn(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except:
            print("###")
    return fn
