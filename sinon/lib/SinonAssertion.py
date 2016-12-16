from .util import ErrorHandler, Wrapper, CollectionHandler
from .SinonSpy import SinonSpy

def checkSpyType(spy):
    if not isinstance(spy, SinonSpy):
        ErrorHandler.assertionIsNotSpyError(spy)

class SinonAssertion(object):

    failException = AssertionError
    message = ""

    @classmethod
    def fail(cls, message):
        SinonAssertion.message = message

    @classmethod
    def notCalled(cls, spy):
        checkSpyType(spy)
        if spy.called:
            raise cls.failException(cls.message)

    @classmethod
    def called(cls, spy):
        checkSpyType(spy)
        if not spy.called:
            raise cls.failException(cls.message)

    @classmethod
    def calledOnce(cls, spy):
        checkSpyType(spy)
        if not spy.calledOnce:
            raise cls.failException(cls.message)

    @classmethod
    def calledTwice(cls, spy):
        checkSpyType(spy)
        if not spy.calledTwice:
            raise cls.failException(cls.message)

    @classmethod
    def calledThrice(cls, spy):
        checkSpyType(spy)
        if not spy.calledThrice:
            raise cls.failException(cls.message)

    @classmethod
    def callCount(cls, spy, n):
        checkSpyType(spy)
        if spy.callCount != n:
            raise cls.failException(cls.message)

    @classmethod
    def callOrder(cls, *args):
        for spy in args:
            checkSpyType(spy)
        for idx, val in enumerate(args):
            if val != args[0] and not val.calledAfter(args[idx-1]):
                raise cls.failException(cls.message)
            if val != args[-1] and not val.calledBefore(args[idx+1]):
                raise cls.failException(cls.message)

    @classmethod
    def calledWith(cls, spy, *args, **kwargs):
        pass

    @classmethod
    def alwaysCalledWith(cls, spy, *args, **kwargs):
        pass

    @classmethod
    def neverCalledWith(cls, spy, *args, **kwargs):
        pass

    @classmethod
    def calledWithExactly(cls, spy, *args, **kwargs):
        pass

    @classmethod
    def alwaysCalledWithExactly(cls, spy, *args, **kwargs):
        pass

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
    def threw(cls, spy, error_type):
        pass

    @classmethod
    def alwaysThrew(cls, spy, error_type):
        pass
