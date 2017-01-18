import sys
sys.path.insert(0, '../')

import unittest
import sinon
from TestClass import ForTestOnly

def A_func():
    pass

def FakeFunc():
    pass

g = sinon.init(globals())

@sinon.test
def test_spy():
    """
    >>> spy = sinon.spy(A_func)
    >>> g.A_func()
    >>> spy.callCount
    1
    >>> spy.calledOnce
    True
    """
    pass

@sinon.test
def test_stub():
    """
    >>> stub = sinon.stub(A_func)
    >>> stub.returns("stub")
    >>> g.A_func()
    "stub"
    """
    pass

@sinon.test
def test_mock():
    """
    >>> mock = sinon.mock(ForTestOnly)
    >>> exp1 = mock.expects("func1").once()
    >>> exp2 = mock.expects("func2").twice()
    >>> fto = ForTestOnly()
    >>> fto.func1()
    >>> exp1.verify()
    True
    >>> exp2.verify()
    False
    >>> mock.verify()
    False
    >>> fto.func2()
    >>> mock.verify()
    True
    """
    pass
