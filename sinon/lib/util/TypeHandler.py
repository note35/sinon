import sys
import inspect
from . import ErrorHandler
from types import ModuleType, FunctionType, BuiltinFunctionType

def is_pure(obj, prop):
    """
    Checking and setting type to PURE
    Args:
        obj: None
        prop: None
    Return:
        Boolean
    """
    return True if (not prop and not obj) else False

def is_module_function(obj, prop):
    """
    Checking and setting type to MODULE_FUNCTION
    Args:
        obj: ModuleType
        prop: FunctionType
    Return:
        Boolean
    Raise:
        propTypeError: When the type of prop is not valid
        propInObjError: When prop is not in the obj(module/class)
        propIsFuncError: When prop is not a callable stuff
    """
    python_version = sys.version_info[0]
    if python_version == 3:
        unicode = str

    if prop and (isinstance(prop, str) or isinstance(prop, unicode)): #property
        if prop in dir(obj):
            if (
                    isinstance(getattr(obj, prop), FunctionType)
                    or isinstance(getattr(obj, prop), BuiltinFunctionType)
                    or inspect.ismethod(getattr(obj, prop))
            ):
            #inspect.ismethod for python2.7
            #isinstance(...) for python3.x
                return True
            else:
                ErrorHandler.propIsFuncError(obj, prop)
        else:
            ErrorHandler.propInObjError(obj, prop)
    elif prop:
        ErrorHandler.propTypeError(prop)
    return False

def is_function(obj):
    """
    Checking and setting type to FUNCTION
    Args:
        obj: FunctionType
    Return:
        Boolean
    """
    return True if obj and isinstance(obj, FunctionType) else False

def is_module(obj):
    """
    Checking and setting type to MODULE
    Args:
        obj: ModuleType / class
        Note: a Instance will be treated as a MODULE
    Return:
        Boolean
    Raise:
        objTypeError: When obj is not valid
    """
    return True if obj and isinstance(obj, ModuleType) or inspect.isclass(obj) else False

def is_instance(obj):
    if obj:
        return True if hasattr(obj, "__class__") else False
    else:
        ErrorHandler.objTypeError(obj)
