'''
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
'''
from .util import Wrapper
from .spy import SinonSpy

class SinonStub(SinonSpy):
    """
    A stub class of any inspector such as stub/expectation
    It provides all spy functions
    It provides functions same as sinonjs. (excluding closure-related function)
    Argument of constructor can be:
    (1) an anonymous function
    (2) an existing function
    (3) a module function
    (4) a module

    All function/module will be replaced into customized or empty function/class
    Able to be assigned special conditions (on which call, with what args, etc.)
    """

    def __init__(self, obj=None, prop=None, func=None):
        super(SinonStub, self).__init__(obj, prop)
        self._stubfunc = func if func else Wrapper.empty_function
        super(SinonStub, self).wrap2stub(self._stubfunc)
        self._copy = self._cond_args = self._cond_kwargs = self._oncall = None
        # Todo: target is a dirty hack
        self._conditions = {"args":[], "kwargs":[], "action": [], "oncall": [], "target": self.obj}            

    def _append_condition(self, sinon_stub_condition, func):
        '''
        Permanently saves the current (volatile) conditions, which would be otherwise lost

        Args:
            sinon_stub_condition: the _SinonStubCondition object that holds the current conditions
            func: returns a value or raises an exception, as specified by the user
        Returns: the SinonStub._conditions dictionary (for convenience)
        '''
        self._conditions["args"].append(sinon_stub_condition._cond_args)
        self._conditions["kwargs"].append(sinon_stub_condition._cond_kwargs)
        self._conditions["oncall"].append(sinon_stub_condition._oncall)
        self._conditions["action"].append(func)
        return self._conditions

    def withArgs(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Adds a condition for when the stub is called. When the condition is met, a special
        return value can be returned. Adds the specified argument(s) into the condition list.

        For example, when the stub function is called with argument 1, it will return "#":
            stub.withArgs(1).returns("#")

        Without returns/throws at the end of the chain of functions, nothing will happen.
        For example, in this case, although 1 is in the condition list, nothing will happen:
            stub.withArgs(1)

        Return:
            a SinonStub object (able to be chained)
        """
        cond_args = args if len(args) > 0 else None
        cond_kwargs = kwargs if len(kwargs) > 0 else None
        copy = self if not self._copy else self._copy
        return _SinonStubCondition(copy=copy, cond_args=cond_args, cond_kwargs=cond_kwargs, oncall=self._oncall)

    def onCall(self, n): #pylint: disable=invalid-name
        """
        Adds a condition for when the stub is called. When the condition is met, a special
        return value can be returned. Adds the specified call number into the condition
        list.

        For example, when the stub function is called the second time, it will return "#":
            stub.onCall(1).returns("#")

        Without returns/throws at the end of the chain of functions, nothing will happen.
        For example, in this case, although 2 is in the condition list, nothing will happen:
            stub.onCall(2)

        Args:
            n: integer, the call # for which we want a special return value.
               The first call has an index of 0.

        Return:
            a SinonStub object (able to be chained)
        """
        cond_oncall = n + 1
        copy = self if not self._copy else self._copy
        return _SinonStubCondition(copy=copy, oncall=cond_oncall, cond_args=self._cond_args, cond_kwargs=self._cond_kwargs)

    def onFirstCall(self): #pylint: disable=invalid-name
        """
        Equivalent to stub.onCall(0)
        """
        return self.onCall(0)

    def onSecondCall(self): #pylint: disable=invalid-name
        """
        Equivalent to stub.onCall(1)
        """
        return self.onCall(1)

    def onThirdCall(self): #pylint: disable=invalid-name
        """
        Equivalent to stub.onCall(2)
        """
        return self.onCall(2)

    def returns(self, obj):
        """
        Customizes the return values of the stub function. If conditions like withArgs or onCall
        were specified, then the return value will only be returned when the conditions are met.

        Args: obj (anything)
        Return: a SinonStub object (able to be chained)
        """
        super(SinonStub, self).wrap2stub(lambda *args, **kwargs: obj)
        return self

    def throws(self, exception=Exception):
        """
        Customizes the stub function to raise an exception. If conditions like withArgs or onCall
        were specified, then the return value will only be returned when the conditions are met.

        Args: exception (by default=Exception, it could be any customized exception)
        Return: a SinonStub object (able to be chained)
        """
        def exception_function(*args, **kwargs):
            raise exception
        super(SinonStub, self).wrap2stub(exception_function)
        return self

class _SinonStubCondition(SinonStub):
    """
    Allows a new SinonStub object to be created each time the end user specifies a new condition. This is necessary
    to mimic the behaviour of Sinon.JS.

    Author: Jonathan Benn
    """

    def __new__(cls, *args, **kwargs):
        """
        Override the __new__ provided by SinonBase, since we don't want to do any function wrapping
        """
        return object.__new__(cls)

    def __init__(self, copy, cond_args, cond_kwargs, oncall):
        """
        Args:
            copy: the original SinonStub object that spawned this one
            cond_args: the args to which a subsequent call to returns/throws should apply
            cond_kwargs: the kwargs to which a subsequent call to returns/throws should apply
            oncall: the integer call number to which a subsequent call to returns/throws should apply
        """
        self._copy = copy
        self._cond_args = cond_args
        self._cond_kwargs = cond_kwargs
        self._oncall = oncall

    def returns(self, obj):
        """
        Customizes the return values of the stub function. If conditions like withArgs or onCall
        were specified, then the return value will only be returned when the conditions are met.

        Args: obj (anything)
        Return: a SinonStub object (able to be chained)
        """
        conditions = self._copy._append_condition(self, lambda *args, **kwargs: obj)
        super(SinonStub, self._copy).wrap2stub(self._copy._stubfunc, conditions)
        return self

    def throws(self, exception=Exception):
        """
        Customizes the stub function to raise an exception. If conditions like withArgs or onCall
        were specified, then the return value will only be returned when the conditions are met.

        Args: exception (by default=Exception, it could be any customized exception)
        Return: a SinonStub object (able to be chained)
        """
        def exception_function(*args, **kwargs):
            raise exception
        conditions = self._copy._append_condition(self, exception_function)
        super(SinonStub, self._copy).wrap2stub(self._copy._stubfunc, conditions)
        return self
