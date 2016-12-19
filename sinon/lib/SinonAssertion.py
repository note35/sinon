from .util import ErrorHandler, Wrapper, CollectionHandler
from .SinonSpy import SinonSpy

class SinonAssertion(object):

    failException = AssertionError
    message = ""

    @classmethod
    def _checkSpyType(cls, spy):
        if not isinstance(spy, SinonSpy):
            ErrorHandler.assertionIsNotSpyError(spy)

    @classmethod
    def _isSatisfied(cls, condition):
        if not condition:
            raise cls.failException(cls.message)

    @classmethod
    def fail(cls, message):
        SinonAssertion.message = message

    @classmethod
    def notCalled(cls, spy):
        cls._checkSpyType(spy)
        cls._isSatisfied(not spy.called)

    @classmethod
    def called(cls, spy):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.called)

    @classmethod
    def calledOnce(cls, spy):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.calledOnce)

    @classmethod
    def calledTwice(cls, spy):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.calledTwice)

    @classmethod
    def calledThrice(cls, spy):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.calledThrice)

    @classmethod
    def callCount(cls, spy, n):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.callCount == n)

    @classmethod
    def callOrder(cls, *args):
        for spy in args:
            cls._checkSpyType(spy)
        for idx, val in enumerate(args):
            if val != args[0]:
                cls._isSatisfied(val.calledAfter(args[idx-1]))
            if val != args[-1]:
                cls._isSatisfied(val.calledBefore(args[idx+1]))

    @classmethod
    def calledWith(cls, spy, *args, **kwargs):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.calledWith(*args, **kwargs))

    @classmethod
    def alwaysCalledWith(cls, spy, *args, **kwargs):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.alwaysCalledWith(*args, **kwargs))
       
    @classmethod
    def neverCalledWith(cls, spy, *args, **kwargs):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.neverCalledWith(*args, **kwargs))

    @classmethod
    def calledWithExactly(cls, spy, *args, **kwargs):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.calledWithExactly(*args, **kwargs))

    @classmethod
    def alwaysCalledWithExactly(cls, spy, *args, **kwargs):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.alwaysCalledWithExactly(*args, **kwargs))

    @classmethod
    def calledWithMatch(cls, spy, *args, **kwargs):
        pass

    @classmethod
    def alwaysCalledWithMatch(cls, spy, *args, **kwargs):
        pass
   
    @classmethod
    def neverCalledWithMatch(cls, spy, *args, **kwargs):
        pass

    @classmethod
    def threw(cls, spy, error_type=None):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.threw(error_type))

    @classmethod
    def alwaysThrew(cls, spy, error_type=None):
        cls._checkSpyType(spy)
        cls._isSatisfied(spy.alwaysThrew(error_type))
