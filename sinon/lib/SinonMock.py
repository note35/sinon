'''
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
'''
import weakref
import inspect
from types import ModuleType, FunctionType

from .SinonStub import SinonStub
from .util import ErrorHandler

class SinonExpectation(SinonStub):
    """
    expectation is expected to ONLY be called by mock
    The implementation of expectation is actually spy/stub
    It provides functions same as sinonjs (excluding closure-related function)
    """

    def __init__(self, obj=None, prop=None):
        """
        Constructor of SinonExpectation

        instance variable:
            valid_list: storing all chained conditions
        """
        super(SinonExpectation, self).__init__(obj, prop)
        self.valid_list = []

    def atLeast(self, number): #pylint: disable=invalid-name
        """
        Inspected function should be called at least number times.
        Args: number
        Return: self
        """
        def check(): #pylint: disable=missing-docstring
            return True if number <= super(SinonExpectation, self).callCount else False
        self.valid_list.append(check)
        return self

    def atMost(self, number): #pylint: disable=invalid-name
        """
        Inspected function should be called at most number times.
        Args: number
        Return: self
        """
        def check(): #pylint: disable=missing-docstring
            return True if number >= super(SinonExpectation, self).callCount else False
        self.valid_list.append(check)
        return self

    def never(self):
        """
        Inspected function should never be called
        Return: self
        """
        def check(): #pylint: disable=missing-docstring
            return not super(SinonExpectation, self).called
        self.valid_list.append(check)
        return self

    def once(self):
        """
        Inspected function should be called one time
        Return: self
        """
        def check(): #pylint: disable=missing-docstring
            return super(SinonExpectation, self).calledOnce
        self.valid_list.append(check)
        return self

    def twice(self):
        """
        Inspected function should be called two times
        Return: self
        """
        def check(): #pylint: disable=missing-docstring
            return super(SinonExpectation, self).calledTwice
        self.valid_list.append(check)
        return self

    def thrice(self):
        """
        Inspected function should be called three times
        Return: self
        """

        def check(): #pylint: disable=missing-docstring
            return super(SinonExpectation, self).calledThrice
        self.valid_list.append(check)
        return self

    def exactly(self, number):
        """
        Inspected function should be called exactly number times
        Return: self
        """
        def check(): #pylint: disable=missing-docstring
            return True if number == super(SinonExpectation, self).callCount else False
        self.valid_list.append(check)
        return self

    def withArgs(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Inspected function should be called with some of specified arguments
        Args: any
        Return: self
        """
        def check(): #pylint: disable=missing-docstring
            return super(SinonExpectation, self).calledWith(*args, **kwargs)
        self.valid_list.append(check)
        return self

    def withExactArgs(self, *args, **kwargs): #pylint: disable=invalid-name
        """
        Inspected function should be called with full of specified arguments
        Args: any
        Return: self
        """
        def check(): #pylint: disable=missing-docstring
            return super(SinonExpectation, self).calledWithExactly(*args, **kwargs)
        self.valid_list.append(check)
        return self

    def verify(self):
        """
        Running all conditions in the instance variable valid_list
        Return:
            True: pass all conditions
            False: fail at more than one condition
        """
        if self not in self._queue:
            return False
        valid = True
        for check in self.valid_list:
            valid = valid & check()
        return valid


class SinonMock(object):
    """
    SinonMock is a container of module/instance/class
    It will monitor all inspectors in instance variable exp_list
    """

    _queue = [] # class-level variables for storing mock

    def __new__(cls, obj=None):
        """
        Constructor of SinonMock
        Args: obj (module/class/instance/None)
        Return: weakref
        """
        if (not obj or obj and
                (isinstance(obj, ModuleType) or inspect.isclass(obj))
                or not isinstance(obj, FunctionType)):
            new = super(SinonMock, cls).__new__(cls)
            cls._queue.append(new)
            new.__init__(obj)
            return weakref.proxy(new)
        else:
            ErrorHandler.mock_type_error(obj)

    def __init__(self, obj=None):
        """
        instance variable:
            exp_list: storing all inspectors
        """
        self.obj = obj
        self.exp_list = []

    def expects(self, prop):
        """
        Adding new property of object as inspector into exp_list
        Args: string (property of object)
        Return: SinonExpectation
        """
        expectation = SinonExpectation(self.obj, prop)
        self.exp_list.append(expectation)
        return expectation

    def verify(self):
        """
        Verifying all inspectors in exp_list
        Return:
            True: pass all inspectors
            False: fail at more than one inspector
        """
        for expectation in self.exp_list:
            if hasattr(expectation, "verify") and not expectation.verify():
                return False
        return True

    def restore(self):
        """
        Destroy all inspectors in exp_list and SinonMock itself
        """
        for expectation in self.exp_list:
            try:
                expectation.restore()
            except ReferenceError:
                pass #ignore removed expectation
        self._queue.remove(self)
