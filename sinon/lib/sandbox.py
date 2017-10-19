'''
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
'''
from .base import SinonBase
from .util.SpyCall import SpyCall

def __clear_assertion_message(obj):
    """
    Clearing assertion message
    """
    setattr(obj, "message", "")

def __clear_item_in_queue(queue):
    """
    Clearing all items in the queue
    Ignoring destroied item
    """
    for item in reversed(queue):
        try:
            item.restore()
        except: #pylint: disable=bare-except
            pass

def sinontest(test_func):
    """
    Wrapping test functions
    """
    properties = ["SinonSpy", "SinonStub", "SinonMock", "SinonAssertion"]
    production_properties = ["spy", "stub", "mock", "assert"]

    def wrapped_func(*args, **kwargs): #pylint: disable=missing-docstring

        # store original _queue
        original_queue = []
        for item in SinonBase._queue: #pylint: disable=protected-access
            original_queue.append(item)

        SpyCall._next_spy_call_id = 0
        ret = test_func(*args, **kwargs)

        # handle indirect use (called by sinon.py)
        for prop in production_properties:
            if "sinon" in test_func.__globals__ and prop in dir(test_func.__globals__["sinon"]):
                if prop == "assert":
                    __clear_assertion_message(getattr(test_func.__globals__["sinon"], prop))
                else:
                    __clear_item_in_queue(getattr(test_func.__globals__["sinon"], prop)._queue) #pylint: disable=protected-access

        # handle direct use
        for prop in properties:
            if prop in test_func.__globals__.keys():
                if prop == "SinonAssertion":
                    __clear_assertion_message(test_func.__globals__[prop])
                else:
                    __clear_item_in_queue(test_func.__globals__[prop]._queue) #pylint: disable=protected-access

        # set original _queue value back
        SinonBase._queue = original_queue #pylint: disable=protected-access

        return ret
    return wrapped_func
