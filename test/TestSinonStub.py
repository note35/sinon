import unittest
import lib.sinon.SinonBase as sinon
from lib.sinon.SinonStub import SinonStub

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

class TestSinonBase(unittest.TestCase):

    @staticmethod
    def my_func(*args, **kwargs):
        return "my_func"

    def setUp(self):
        sinon.init(globals())

    def test200_constructor_object_method_with_replaced_method(self):
        a = A_object()
        stub = SinonStub(a, "A_func", TestSinonBase.my_func)
        self.assertEqual(a.A_func(), "my_func")
        stub.restore()

    def test201_constructor_empty_object(self):
        stub = SinonStub(A_object)
        a = sinon.g.A_object()
        self.assertTrue("A_func" not in dir(a))
        stub.restore()

    def test202_constructor_empty_outside_function(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        self.assertEqual(fto.func1(), None)
        stub.restore()

    def test203_constructor_empty_outside_instance_function(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(fto, "func1")
        self.assertEqual(fto.func1(), None)
        stub.restore()

    def test204_constructor_empty_library_function(self):
        self.assertEqual(os.system("cd"), 0)
        stub = SinonStub(os, "system", TestSinonBase.my_func)
        self.assertEqual(os.system("cd"), "my_func")
        stub.restore()
        self.assertEqual(os.system("cd"), 0)

    def test220_returns(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.returns(1)
        self.assertEqual(fto.func1(), 1)
        stub.returns({})
        self.assertEqual(fto.func1(), {})
        stub.returns(TestSinonBase.my_func)
        self.assertEqual(fto.func1(), TestSinonBase.my_func)  
        stub.restore()

    def test221_throws(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.throws()
        with self.assertRaises(Exception) as context:
            fto.func1()
        stub.throws(TypeError)
        with self.assertRaises(TypeError) as context:
            fto.func1()
        stub.restore()

    def test222_withArgs(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.withArgs(1).returns("#")
        self.assertEqual(fto.func1(1), "#")
        stub.withArgs(b=1).returns("##")
        self.assertEqual(fto.func1(b=1), "##")
        stub.withArgs(1, b=1).returns("###")
        self.assertEqual(fto.func1(1, b=1), "###")
        self.assertEqual(fto.func1(2), None)
        stub.restore()

    def test223_onCall(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.onCall(3).returns("oncall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "oncall") #3 will return oncall
        stub.onCall(2).returns("oncall") # the callCount will be reset to 0
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "oncall") #2 will return oncall
        self.assertEqual(fto.func1(), "oncall") #3 will still return oncall
        stub.restore()

    def test224_onCall_withArgs(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.withArgs(1).onCall(3).returns("oncall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(1), "oncall")
        stub.withArgs(2).onCall(2).returns("oncall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(2), "oncall")
        stub.restore()

    def test225_onCall_plus_withArgs(self):
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        stub = SinonStub(ForTestOnly, "func1")
        stub.withArgs(1).returns("1")
        self.assertEqual(fto.func1(1), "1")
        stub.withArgs(1).onCall(2).returns("oncall")
        self.assertEqual(fto.func1(1), "1")
        self.assertEqual(fto.func1(1), "oncall")
        stub.onCall(3).returns("###")
        self.assertEqual(fto.func1(1), "1")
        self.assertEqual(fto.func1(1), "oncall")
        self.assertEqual(fto.func1(1), "1") # the priority of onCall is lower than withArgs
        stub.onCall(2).returns("##")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "##")
        self.assertEqual(fto.func1(), "###")
        stub.restore()

    def test230_onFirstCall(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.onFirstCall().returns("onFirstCall")
        self.assertEqual(fto.func1(), "onFirstCall")
        stub.restore()

    def test231_onSecondCall(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.onSecondCall().returns("onSecondCall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "onSecondCall")
        stub.restore()

    def test232_onThirdCall(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.onThirdCall().returns("onThirdCall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), "onThirdCall")
        stub.restore()

    def test233_onThirdCall_random_args(self):
        fto = ForTestOnly()
        stub = SinonStub(ForTestOnly, "func1")
        stub.onThirdCall().returns("onThirdCall")
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(), None)
        self.assertEqual(fto.func1(1), "onThirdCall")
        stub.restore()
