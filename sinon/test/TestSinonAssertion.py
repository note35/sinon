import sys
sys.path.insert(0, '../')

import unittest
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
"""
======================================================
                 FOR TEST ONLY END
======================================================
"""

class TestSinonAssertion(unittest.TestCase):

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
        exception = "[{}] is an invalid spy".format("1234")
        with self.assertRaises(Exception) as context:
            SinonAssertion.notCalled("1234")
        self.assertTrue(exception in str(context.exception))

    @sinontest
    def test005_arg_bool(self):
        exception = "[{}] is an invalid spy".format(True)
        with self.assertRaises(Exception) as context:
            SinonAssertion.notCalled(True)
        self.assertTrue(exception in str(context.exception))

    @sinontest
    def test006_fail_new_message(self):
        spy = SinonSpy(os, "system")
        exception_msg = "Hahaha"
        SinonAssertion.fail(exception_msg)
        with self.assertRaises(Exception) as context:
            SinonAssertion.called(spy)
        self.assertTrue(exception_msg in str(context.exception))

    @sinontest
    def test040_callOrder_only_one_arg(self):
        spy = SinonSpy()
        SinonAssertion.callOrder(spy)

    @sinontest
    def test040_callOrder_two_unique_args(self):
        spy1 = SinonSpy()
        stub1 = SinonStub()
        spy1()
        stub1()
        SinonAssertion.callOrder(spy1, stub1)

    @sinontest
    def test040_callOrder_three_unique_args_call_repeated(self):
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
