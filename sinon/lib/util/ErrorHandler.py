def exceptionHelper(msg, debug=False, exception=Exception):
    if debug:
        print (msg)
        return msg
    else:
        raise exception(msg)
        return None

def objTypeError(obj):
    return exceptionHelper("[{}] is an invalid module/class/function".format(str(obj)))

def mockTypeError(obj):
    return exceptionHelper("[{}] is an invalid module/class".format(str(obj)))

def propTypeError(prop):
    return exceptionHelper("[{}] is an invalid property, it should be a string".format(prop)) 

def propIsNotAFuncError(obj, prop):
    return exceptionHelper("[{}] is an invalid property, it should be a method in [{}]".format(prop, obj.__name__))

def propInObjError(obj, prop):
    return exceptionHelper("[{}] is not exist in [{}]".format(prop, obj.__name__))

def lockError(name):
    return exceptionHelper("[{}] have already been declared".format(name))

def calledWithEmptyError():
    return exceptionHelper("calledWith() have no argument")

def getCallIndexError(n):
    return exceptionHelper("The call queue only contains {} calls".format(str(n)), exception=IndexError)
