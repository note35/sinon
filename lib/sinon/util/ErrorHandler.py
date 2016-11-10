def exceptionHelper(msg, debug=False):
    if debug:
        print (msg)
        return msg
    else:
        raise Exception(msg)
        return None

def objTypeError(obj):
    return exceptionHelper("[{}] is an invalid module/class/function".format(str(obj)))

def propTypeError(prop):
    return exceptionHelper("[{}] is an invalid property, it should be a string".format(prop)) 

def propInObjError(obj, prop):
    return exceptionHelper("[{}] is not exist in [{}]".format(prop, obj.__name__))

def lockError(name):
    return exceptionHelper("[{}] have already been declared".format(name))

def calledWithEmptyError():
    return exceptionHelper("calledWith() have no argument")
