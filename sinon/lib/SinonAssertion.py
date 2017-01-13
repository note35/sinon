"""
Copyright (c) 2016-2017, Kir Chou
https://github.com/note35/sinon/blob/master/LICENSE
"""
from .util import ErrorHandler
from .SinonSpy import SinonSpy

class SinonAssertion(object):
    """
    assertion is an API for external to verify inspector(s)
    """

    failException = AssertionError
    message = ""

    @classmethod
    def __is_spy(cls, spy):
        """
        checking the argument is spy
        Args: SinonSpy
        Raised: assertionIsNotSpyError (if argument is not spy/stub/expectation)
        """
        if not isinstance(spy, SinonSpy):
            ErrorHandler.assertionIsNotSpyError(spy)

    @classmethod
    def __is_satisfied(cls, condition):
        """
        checking if condition is be satisfied
        Raised: customized exception
        """
        if not condition:
            raise cls.failException(cls.message)

    @classmethod
    def fail(cls, message):
        """
        Defining fail message of assertion
        This function will change message until all tests finished
        Args: str
        """
        SinonAssertion.message = message

    @classmethod
    def notCalled(cls, spy): #pylint: disable=invalid-name
        """
        Checking the inspector is not called
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(not spy.called)

    @classmethod
    def called(cls, spy):
        """
        Checking the inspector is called
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.called)

    @classmethod
    def calledOnce(cls, spy): #pylint: disable=invalid-name
        """
        Checking the inspector is called once
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.calledOnce)

    @classmethod
    def calledTwice(cls, spy): #pylint: disable=invalid-name
        """
        Checking the inspector is called twice
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.calledTwice)

    @classmethod
    def calledThrice(cls, spy): #pylint: disable=invalid-name
        """
        Checking the inspector is called thrice
        Args: SinonSpy
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.calledThrice)

    @classmethod
    def callCount(cls, spy, number): #pylint: disable=invalid-name
        """
        Checking the inspector is called number times
        Args: SinonSpy, number
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.callCount == number)

    @classmethod
    def callOrder(cls, *args): #pylint: disable=invalid-name
        """
        Checking the inspector is called with given priority
        Args: SinonSpy, list of inspectors
        eg.
            [spy1, spy2, spy3] => spy1 is called before spy2, spy2 is called before spy3
            [spy1, spy2, spy1] => spy1 is called before and after spy2
        """
        for spy in args:
            cls.__is_spy(spy)
        for idx, val in enumerate(args):
            if val != args[0]:
                cls.__is_satisfied(val.calledAfter(args[idx-1]))
            if val != args[-1]:
                cls.__is_satisfied(val.calledBefore(args[idx+1]))

    @classmethod
    def calledWith(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is called with partial args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.calledWith(*args, **kwargs))

    @classmethod
    def alwaysCalledWith(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is always called with partial args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.alwaysCalledWith(*args, **kwargs))

    @classmethod
    def neverCalledWith(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is never called with partial args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.neverCalledWith(*args, **kwargs))

    @classmethod
    def calledWithExactly(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is called with exactly args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.calledWithExactly(*args, **kwargs))

    @classmethod
    def alwaysCalledWithExactly(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is always called with exactly args/kwargs
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.alwaysCalledWithExactly(*args, **kwargs))

    @classmethod
    def calledWithMatch(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is called with partial SinonMatcher(args/kwargs)
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.calledWithMatch(*args, **kwargs))

    @classmethod
    def alwaysCalledWithMatch(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is always called with partial SinonMatcher(args/kwargs)
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.alwaysCalledWithMatch(*args, **kwargs))

    @classmethod
    def neverCalledWithMatch(cls, spy, *args, **kwargs): #pylint: disable=invalid-name
        """
        Checking the inspector is never called with partial SinonMatcher(args/kwargs)
        Args: SinonSpy, args/kwargs
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.neverCalledWithMatch(*args, **kwargs))

    @classmethod
    def threw(cls, spy, error_type=None):
        """
        Checking the inspector is raised error_type
        Args: SinonSpy, Exception (defaut: None)
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.threw(error_type))

    @classmethod
    def alwaysThrew(cls, spy, error_type=None): #pylint: disable=invalid-name
        """
        Checking the inspector is always raised error_type
        Args: SinonSpy, Exception (defaut: None)
        """
        cls.__is_spy(spy)
        cls.__is_satisfied(spy.alwaysThrew(error_type))
