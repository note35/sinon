"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE

A set of functions for handling known error
"""

def __exception_helper(msg, exception=Exception): #pylint: disable=missing-docstring
    raise exception(msg)

def mock_type_error(obj): #pylint: disable=missing-docstring
    error_msg = "[{}] is an invalid module/class".format(str(obj))
    return __exception_helper(error_msg)

def prop_type_error(prop): #pylint: disable=missing-docstring
    error_msg = "[{}] is an invalid property, it should be a string".format(prop)
    return __exception_helper(error_msg)

def prop_is_func_error(obj, prop): #pylint: disable=missing-docstring
    name = obj.__name__ if hasattr(obj, "__name__") else obj
    error_msg = "[{}] is an invalid property, it should be a method in [{}]".format(prop, name)
    return __exception_helper(error_msg)

def prop_in_obj_error(obj, prop): #pylint: disable=missing-docstring
    error_msg = "[{}] is not exist in [{}]".format(prop, obj)
    return __exception_helper(error_msg)

def lock_error(obj): #pylint: disable=missing-docstring
    name = obj.__name__ if hasattr(obj, "__name__") else obj
    error_msg = "[{}] have already been declared".format(name)
    return __exception_helper(error_msg)

def called_with_empty_error(): #pylint: disable=missing-docstring
    error_msg = "There is no argument"
    return __exception_helper(error_msg)

def is_not_spy_error(obj): #pylint: disable=missing-docstring
    error_msg = "[{}] is an invalid spy".format(str(obj))
    return __exception_helper(error_msg)

def matcher_type_error(prop): #pylint: disable=missing-docstring
    error_msg = "[{}] is an invalid property, it should be a type".format(prop)
    return __exception_helper(error_msg, exception=TypeError)

def matcher_instance_error(prop): #pylint: disable=missing-docstring
    error_msg = "[{}] is an invalid property, it should be an instance".format(prop)
    return __exception_helper(error_msg, exception=TypeError)

def wrapper_object_not_found_error():
    error_msg = 'Wrapper object cannot be found'
    return __exception_helper(error_msg)
