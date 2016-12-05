import unittest
import lib.sinon.SinonBase as sinon
from lib.sinon.SinonSpy import SinonSpy
from lib.sinon.SinonStub import SinonStub
from lib.sinon.SinonSandbox import sinontest

"""
======================================================
                 FOR TEST ONLY START
======================================================
"""
# build-in module
import os
# customized class
class A_object(object):
    # customized function
    def A_func(self):
        return "test_global_A_func"

# global function
def B_func(x=None):
    if x:
        return "test_local_B_func"+str(x)
    return "test_local_B_func"

def C_func(a="a", b="b", c="c"):
    return "test_local_C_func"

def D_func(err=False):
    if err:
        raise err
    else:
        return "test_local_D_func"

from TestClass import ForTestOnly

"""
======================================================
                 FOR TEST ONLY END
======================================================
"""



class TestSinonSandbox(unittest.TestCase):

    def setUp(self):
        sinon.init(globals())

    @classmethod
    @sinontest
    def _spy_in_sinontest(self):
        base1 = SinonSpy(ForTestOnly)
        base2 = SinonSpy(D_func)
        base3 = SinonSpy(A_object)
   
    @classmethod
    @sinontest
    def _stub_in_sinontest(self):
        base1 = SinonStub(ForTestOnly)
        base2 = SinonStub(D_func)
        base3 = SinonStub(A_object)

    def test001_test_spy_in_sinontest(self):
        base = SinonSpy()
        self.assertEqual(len(base._queue), 2)
        TestSinonSandbox._spy_in_sinontest()
        exception = "weakly-referenced object no longer exists"
        with self.assertRaises(Exception) as context:
            base.called
        self.assertTrue(exception in str(context.exception))

    def test002_test_stub_in_sinontest(self):
        base = SinonStub()
        self.assertEqual(len(base._queue), 1)
        TestSinonSandbox._stub_in_sinontest()
        exception = "weakly-referenced object no longer exists"
        with self.assertRaises(Exception) as context:
            base.called
        self.assertTrue(exception in str(context.exception))
