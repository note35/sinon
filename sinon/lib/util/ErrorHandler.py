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

def propIsFuncError(obj, prop):
    return exceptionHelper("[{}] is an invalid property, it should be a method in [{}]".format(prop, obj.__name__))

def propInObjError(obj, prop):
    name = obj.__name__ if hasattr(obj, "__name__") else obj
    return exceptionHelper("[{}] is not exist in [{}]".format(prop, obj))

def lockError(obj):
    name = obj.__name__ if hasattr(obj, "__name__") else obj
    return exceptionHelper("[{}] have already been declared".format(name))

def calledWithEmptyError():
    return exceptionHelper("There is no argument")

def getCallIndexError(n):
    return exceptionHelper("The call queue only contains {} calls".format(str(n)), exception=IndexError)

def assertionIsNotSpyError(obj):
    return exceptionHelper("[{}] is an invalid spy".format(str(obj)))

def callQueueIsEmptyError():
    return exceptionHelper("CALLQUEUE is empty")

def matcherTypeError(prop):
    return exceptionHelper("[{}] is an invalid property, it should be a type".format(prop), exception=TypeError)

def matcherInstanceError(prop):
    return exceptionHelper("[{}] is an invalid property, it should be an instance".format(prop), exception=TypeError)
