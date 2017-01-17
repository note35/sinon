import sys
sys.path.insert(0, '../')

import unittest
import lib.SinonBase as sinon
from lib.SinonAssertion import SinonAssertion
from lib.SinonSpy import SinonSpy
from lib.SinonStub import SinonStub
from lib.SinonMock import SinonMock
from lib.SinonSandbox import sinontest

"""
======================================================
                 FOR TEST ONLY START
======================================================
"""
# build-in module
import os

# global function
def C_func(a="a", b="b", c="c"):
    return "test_local_C_func"

def D_func(err=False):
    if err:
        raise err
    else:
        return "test_local_D_func"
"""
======================================================
                 FOR TEST ONLY END
======================================================
"""

class TestSinonAssertion(unittest.TestCase):

    def setUp(self):
        sinon.g = sinon.init(globals())

    @sinontest
    def test001_arg_spy(self):
        spy = SinonSpy(os, "system")
        SinonAssertion.notCalled(spy)

    @sinontest
    def test002_arg_stub(self):
        stub = SinonStub(os, "system")
        SinonAssertion.notCalled(stub)

    @sinontest
    def test003_arg_expectation(self):
        mock = SinonMock(os)
        exp = mock.expects("system")
        SinonAssertion.notCalled(exp)

    @sinontest
    def test004_arg_string(self):
        with self.assertRaises(Exception) as context:
            SinonAssertion.notCalled("1234")

    @sinontest
    def test005_arg_bool(self):
        with self.assertRaises(Exception) as context:
            SinonAssertion.notCalled(True)

    @sinontest
    def test006_fail_new_message(self):
        spy = SinonSpy(os, "system")
        exception_msg = "Hahaha"
        SinonAssertion.fail(exception_msg)
        with self.assertRaises(Exception) as context:
            SinonAssertion.called(spy)
        self.assertTrue(exception_msg in str(context.exception)) #test new errmsg

    @sinontest
    def test010_notCalled(self):
        spy = SinonSpy(os, "system")
        SinonAssertion.notCalled(spy)
        os.system("cd")
        with self.assertRaises(Exception) as context:
            SinonAssertion.notCalled(spy)

    @sinontest
    def test011_called(self):
        spy = SinonSpy(os, "system")
        with self.assertRaises(Exception) as context:
            SinonAssertion.called(spy)
        os.system("cd")
        SinonAssertion.called(spy)

    @sinontest
    def test012_calledOnce(self):
        spy = SinonSpy(os, "system")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledOnce(spy)
        os.system("cd")
        SinonAssertion.calledOnce(spy)
        os.system("cd")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledOnce(spy)

    @sinontest
    def test013_calledTwice(self):
        spy = SinonSpy(os, "system")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledTwice(spy)
        os.system("cd")
        os.system("cd")
        SinonAssertion.calledTwice(spy)

    @sinontest
    def test014_calledThrice(self):
        spy = SinonSpy(os, "system")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledThrice(spy)
        os.system("cd")
        os.system("cd")
        os.system("cd")
        SinonAssertion.calledThrice(spy)

    @sinontest
    def test015_callCount(self):
        spy = SinonSpy(os, "system")
        SinonAssertion.callCount(spy, 0)
        os.system("cd")
        SinonAssertion.callCount(spy, 1)
        for i in range(10):
            os.system("cd")
        SinonAssertion.callCount(spy, 11)

    @sinontest
    def test040_callOrder_only_one_arg(self):
        spy = SinonSpy()
        spy()
        SinonAssertion.callOrder(spy)

    @sinontest
    def test041_callOrder_two_unique_args_without_call(self):
        spy1 = SinonSpy()
        stub1 = SinonStub()
        with self.assertRaises(Exception) as context:
            SinonAssertion.callOrder(spy1, stub1)

    @sinontest
    def test042_callOrder_two_unique_args(self):
        spy1 = SinonSpy()
        stub1 = SinonStub()
        spy1()
        stub1()
        SinonAssertion.callOrder(spy1, stub1)

    @sinontest
    def test043_callOrder_three_unique_args_call_repeated(self):
        spy1 = SinonSpy()
        stub1 = SinonStub()
        spy2 = SinonSpy()
        spy1()
        stub1()
        spy2()
        spy1()
        SinonAssertion.callOrder(spy1, stub1, spy2)
        SinonAssertion.callOrder(spy1, stub1, spy2, spy1)
        SinonAssertion.callOrder(stub1, spy2, spy1)
        SinonAssertion.callOrder(stub1, spy1)
        SinonAssertion.callOrder(spy1, stub1)
        SinonAssertion.callOrder(spy2, spy1)
        SinonAssertion.callOrder(spy1, spy2)

    @sinontest
    def test050_calledWith_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        SinonAssertion.calledWith(spy, "a", "b", "c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWith(spy, "a", "wrong", "c")

    @sinontest
    def test051_calledWith_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        SinonAssertion.calledWith(spy, a="a", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWith(spy, a="wrong", b="b", c="c")

    @sinontest
    def test052_calledWith_both(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", b="b", c="c")
        SinonAssertion.calledWith(spy, "a", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWith(spy, "a", "b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWith(spy, "a", "b", "c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWith(spy, "a", "b", "d")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWith(spy, "a", "b", c="d")

    @sinontest
    def test060_alwaysCalledWith_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "xxxx")
        SinonAssertion.alwaysCalledWith(spy, "a", "b")
        sinon.g.C_func("d", "e", "f")
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWith(spy, "a", "b")

    @sinontest
    def test061_alwaysCalledWith_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="xxxx", b="b", c="c")
        SinonAssertion.alwaysCalledWith(spy, b="b", c="c")
        sinon.g.C_func(a="d", b="e", c="f")
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWith(spy, b="b", c="c")

    @sinontest
    def test062_alwaysCalledWith_both(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b")
        SinonAssertion.alwaysCalledWith(spy, "a", b="b")
        sinon.g.C_func("b", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWith(spy, "a", b="b")

    @sinontest
    def test070_neverCalledWith_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.neverCalledWith(spy, "a", "b", "c")
        SinonAssertion.neverCalledWith(spy, "a", "wrong", "c")

    @sinontest
    def test071_neverCalledWith_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.neverCalledWith(spy, a="a", b="b", c="c")
        SinonAssertion.neverCalledWith(spy, a="wrong", b="b", c="c")

    @sinontest
    def test072_neverCalledWith_both(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.neverCalledWith(spy, "a", b="b", c="c")
        SinonAssertion.neverCalledWith(spy, "a", "b", c="c")
        SinonAssertion.neverCalledWith(spy, "a", "b", "c")
        SinonAssertion.neverCalledWith(spy, "a", "b", "d")
        SinonAssertion.neverCalledWith(spy, "a", "b", c="d")

    @sinontest
    def test080_calledWithExactly_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        SinonAssertion.calledWithExactly(spy, "a", "b", "c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithExactly(spy, "d", "e", "f")

    @sinontest
    def test081_calledWithExactly_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        SinonAssertion.calledWithExactly(spy, a="a", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithExactly(spy, a="d", b="e", c="f")

    @sinontest
    def test082_calledWithExactly_both(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", b="b", c="c")
        SinonAssertion.calledWithExactly(spy, "a", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithExactly(spy, "wrong", b="b", c="c")

    @sinontest
    def test090_alwaysCalledWithExactly_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        SinonAssertion.alwaysCalledWithExactly(spy, "a", "b", "c")
        sinon.g.C_func("a", "b", "xxxx")
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWithExactly(spy, "a", "b", "c")

    @sinontest
    def test091_alwaysCalledWithExactly_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        SinonAssertion.alwaysCalledWithExactly(spy, a="a", b="b", c="c")
        sinon.g.C_func(a="xxxx", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWithExactly(spy, a="a", b="b", c="c")

    @sinontest
    def test092_alwaysCalledWithExactly_both(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        SinonAssertion.alwaysCalledWithExactly(spy, "a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="xxx")
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWithExactly(spy, "a", b="b", c="c")

    @sinontest
    def test100_calledWithMatch_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        SinonAssertion.calledWithMatch(spy, str, str, "c")
        SinonAssertion.calledWithMatch(spy, str, str)
        SinonAssertion.calledWithMatch(spy, str)
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithMatch(spy, "a", "wrong", "c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithMatch(spy, int, "b", "c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithMatch(spy, str, int)

    @sinontest
    def test101_calledWithMatch_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        SinonAssertion.calledWithMatch(spy, a=str, b=str, c="c")
        SinonAssertion.calledWithMatch(spy, a=str, b=str)
        SinonAssertion.calledWithMatch(spy, a=str)
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithMatch(spy, a="wrong", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithMatch(spy, a=int, b=int, c=int)
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithMatch(spy, a=str, b=int)

    @sinontest
    def test0102_calledWithMatch_both(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", b="b", c="c")
        SinonAssertion.calledWithMatch(spy, str, b=str, c=str)
        SinonAssertion.calledWithMatch(spy, str, b=str)
        SinonAssertion.calledWithMatch(spy, str, c=str)
        SinonAssertion.calledWithMatch(spy, b=str, c=str)
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithMatch(spy, str, str, c=str)
        with self.assertRaises(Exception) as context:
            SinonAssertion.calledWithMatch(spy, str, str, str)

    @sinontest
    def test110_alwaysCalledWithMatch_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "xxxx")
        SinonAssertion.alwaysCalledWithMatch(spy, str, str, str)
        sinon.g.C_func("d", "e", 123)
        SinonAssertion.alwaysCalledWithMatch(spy, str, str)
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWithMatch(spy, str, str, str)

    @sinontest
    def test111_alwaysCalledWithMatch_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="xxxx", b="b", c="c")
        SinonAssertion.alwaysCalledWithMatch(spy, b=str, c=str)
        sinon.g.C_func(a="d", b="e", c=123)
        SinonAssertion.alwaysCalledWithMatch(spy, a=str, b=str)
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWithMatch(spy, b=str, c=str)

    @sinontest
    def test112_alwaysCalledWithMatch_both(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b")
        SinonAssertion.alwaysCalledWithMatch(spy, str, b=str)
        sinon.g.C_func("b", b="b", c=123)
        SinonAssertion.alwaysCalledWithMatch(spy, str, b=str)
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysCalledWithMatch(spy, str, c=str)

    @sinontest
    def test120_neverCalledWithMatch_args(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", "b", "c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.neverCalledWithMatch(spy, str, str, str)
        SinonAssertion.neverCalledWithMatch(spy, int, int, int)

    @sinontest
    def test121_neverCalledWithMatch_kwargs(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func(a="a", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.neverCalledWithMatch(spy, a=str, b=str, c=str)
        SinonAssertion.neverCalledWithMatch(spy, a=int, b=str, c=str)

    @sinontest
    def test122_neverCalledWithMatch_both(self):
        spy = SinonSpy(C_func)
        sinon.g.C_func("a", b="b", c="c")
        with self.assertRaises(Exception) as context:
            SinonAssertion.neverCalledWithMatch(spy, str, b=str, c=str)
        SinonAssertion.neverCalledWithMatch(spy, int, int, c=int)
        SinonAssertion.neverCalledWithMatch(spy, int, int, int)

    @sinontest
    def test130_threw_default_type(self):
        spy = SinonSpy(D_func)

        # Without any exception
        with self.assertRaises(Exception) as context:
            SinonAssertion.threw(spy, ValueError)

        # With an exception
        try:
            sinon.g.D_func(err=ValueError)
        except:
            SinonAssertion.threw(spy)
            SinonAssertion.threw(spy, ValueError)

    @sinontest
    def test131_threw_custom_type(self):
        class MyException(Exception):
            pass
        spy = SinonSpy(D_func)

        # Without any exception
        with self.assertRaises(Exception) as context:
            SinonAssertion.threw(spy, MyException)

        # With an exception
        try:
            sinon.g.D_func(err=MyException)
        except:
            SinonAssertion.threw(spy)
            SinonAssertion.threw(spy, MyException)

    @sinontest
    def test132_threw_no_error(self):
        spy = SinonSpy(D_func)
        sinon.g.D_func(err=False)
        with self.assertRaises(Exception) as context:
            SinonAssertion.threw(spy) 

    @sinontest
    def test140_alwaysThrew_default_type(self):
        spy = SinonSpy(D_func)

        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysThrew(spy)
        with self.assertRaises(Exception) as context:
            SinonAssertion.alwaysThrew(spy, ValueError)

        # With exceptions
        try:
            sinon.g.D_func(err=ValueError)
        except:
            SinonAssertion.alwaysThrew(spy)
            SinonAssertion.alwaysThrew(spy, ValueError)
        try:
            sinon.g.D_func(err=ValueError)
        except:
            SinonAssertion.alwaysThrew(spy)
            SinonAssertion.alwaysThrew(spy, ValueError)

        # With a new exception
        try:
            sinon.g.D_func(err=TypeError)
        except:
            SinonAssertion.alwaysThrew(spy)
            with self.assertRaises(Exception) as context:
                SinonAssertion.alwaysThrew(spy, ValueError)
