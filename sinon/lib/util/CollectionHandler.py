"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE

A set of functions for handling SinonSpy's calledWithXXX functions
"""

def tuple_in_list(main, sub):
    """
    >>> main = [('a', 'b', 'c'), ('c', 'd')]
    >>> tuple_in_list(main, ('a',))
    False
    >>> tuple_in_list(main, ('b','d'))
    False
    >>> tuple_in_list(main, ('a','b','c'))
    True
    >>> tuple_in_list(main, ('c','d'))
    True
    >>> tuple_in_list(main, ('z',))
    False
    >>> tuple_in_list(main, ((),))
    False
    """
    return obj_in_list(main, sub)

def dict_in_list(main, sub):
    """
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'd': 'd'}]
    >>> dict_in_list(main, {'c': 'c'})
    False
    >>> dict_in_list(main, {'b': 'b', 'd': 'd'})
    False
    >>> dict_in_list(main, {'c': 'c', 'a': 'a', 'b': 'b'})
    True
    >>> dict_in_list(main, {'c': 'c', 'd': 'd'})
    True
    >>> dict_in_list(main, {'z': 'z'})
    False
    >>> dict_in_list(main, {})
    False
    """
    return obj_in_list(main, sub)

def tuple_in_list_always(main, sub):
    """
    >>> main = [('a', 'b', 'c'), ('c', 'd')]
    >>> tuple_in_list_always(main, ('a' ,'b', 'c'))
    False
    >>> tuple_in_list_always(main, ('c', 'd'))
    False
    >>> tuple_in_list_always(main, ('a', 'c'))
    False
    >>> tuple_in_list_always(main, ('a'))
    False
    >>> tuple_in_list_always(main, ((),))
    False
    >>> main = [('a', 'b', 'c'), ('a', 'b', 'c')]
    >>> tuple_in_list_always(main, ('a' ,'b', 'c'))
    True
    >>> main = [('a', 'b', 'c')]
    >>> tuple_in_list_always(main, ('a' ,'b', 'c'))
    True
    """
    return True if sub in set(main) and len(set(main)) == 1 else False

def dict_in_list_always(main, sub):
    """
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'd': 'd'}]
    >>> dict_in_list_always(main, {'a': 'a', 'b': 'b', 'c': 'c'})
    False
    >>> dict_in_list_always(main, {'c': 'c', 'd': 'd'})
    False
    >>> dict_in_list_always(main, {'a': 'a', 'c': 'c'})
    False
    >>> dict_in_list_always(main, {'a': 'a'})
    False
    >>> dict_in_list_always(main, {})
    False
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}, {'c': 'c', 'a': 'a', 'b': 'b'}]
    >>> dict_in_list_always(main, {'c': 'c', 'a': 'a', 'b': 'b'})
    True
    >>> main = [{'c': 'c', 'a': 'a', 'b': 'b'}]
    >>> dict_in_list_always(main, {'c': 'c', 'a': 'a', 'b': 'b'})
    True
    """
    for item in main:
        if sub != item:
            return False
    return True

def obj_in_list(target_list, obj):
    """
    >>> l = [1,2,3,4]
    >>> obj_in_list(l, 2)
    True
    >>> obj_in_list(l, 5)
    False
    """
    return True if obj in target_list else False

def obj_in_list_always(target_list, obj):
    """
    >>> l = [1,1,1]
    >>> obj_in_list_always(l, 1)
    True
    >>> l.append(2)
    >>> obj_in_list_always(l, 1)
    False
    """
    for item in set(target_list):
        if item is not obj:
            return False
    return True

def dict_partial_cmp(target_dict, dict_list, ducktype):
    """
    Whether partial dict are in dict_list or not
    """
    for called_dict in dict_list:
        # ignore invalid test case
        if len(target_dict) > len(called_dict):
            continue
        # get the intersection of two dicts
        intersection = {}
        for item in target_dict:
            dtype = ducktype(target_dict[item])
            if hasattr(dtype, "mtest"):
                if item in called_dict and dtype.mtest(called_dict[item]):
                    intersection[item] = target_dict[item]
            else:
                if item in called_dict and dtype == called_dict[item]:
                    intersection[item] = target_dict[item]
        if intersection == target_dict:
            return True
    # if no any arguments matched to called_args, return False
    return False

def dict_partial_cmp_always(target_dict, dict_list, ducktype):
    """
    Whether partial dict are always in dict_list or not
    """
    res = []
    for called_dict in dict_list:
        # ignore invalid test case
        if len(target_dict) > len(called_dict):
            continue
        # get the intersection of two dicts
        intersection = {}
        for item in target_dict:
            dtype = ducktype(target_dict[item])
            if hasattr(dtype, "mtest"):
                if item in called_dict and dtype.mtest(called_dict[item]):
                    intersection[item] = target_dict[item]
            else:
                if item in called_dict and dtype == called_dict[item]:
                    intersection[item] = target_dict[item]
        ret = True if intersection == target_dict else False
        res.append(ret)
    # if no any arguments matched to called_args, return False
    return True if res and False not in res else False

def tuple_partial_cmp(target_tuple, tuple_list, ducktype):
    """
    Whether partial target_tuple are in tuple_list or not
    """
    for called_tuple in tuple_list:
        # ignore invalid test case
        if len(target_tuple) > len(called_tuple):
            continue
        # loop all argument from "current arguments"
        dst = len(target_tuple)
        for idx, part_target_tuple in enumerate(target_tuple):
            # test current argument one by one, if matched to previous record, counter-1
            dtype = ducktype(part_target_tuple)
            if hasattr(dtype, "mtest"):
                if dtype.mtest(called_tuple[idx]):
                    dst = dst - 1
            else:
                if dtype == called_tuple[idx]:
                    dst = dst - 1
        # if counter is zero => arguments is partial matched => return True
        if not dst:
            return True
    # if no any arguments matched to called_tuple, return False
    return False

def tuple_partial_cmp_always(target_tuple, tuple_list, ducktype):
    """
    Whether partial target_tuple are always in tuple_list or not
    """
    res = []
    for called_tuple in tuple_list:
        # ignore invalid test case
        if len(target_tuple) > len(called_tuple):
            continue
        # loop all argument from "current arguments"
        dst = len(target_tuple)
        for idx, part_target_tuple in enumerate(target_tuple):
            # test current argument one by one, if matched to previous record, counter-1
            dtype = ducktype(part_target_tuple)
            if hasattr(dtype, "mtest"):
                if dtype.mtest(called_tuple[idx]):
                    dst = dst - 1
            else:
                if dtype == called_tuple[idx]:
                    dst = dst - 1
        # if counter is zero => arguments is partial matched => return True
        ret = True if not dst else False
        res.append(ret)
    # if no any arguments matched to called_tuple, return False
    return True if res and False not in res else False
