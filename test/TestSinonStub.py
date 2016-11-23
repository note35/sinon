import sys
sys.path.insert(0, '../')

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

    def setUp(self):
        sinon.init(globals())

    def test200_constructor_object_method_with_replaced_method(self):
        def my_func():
            return "my_func"
        a = A_object()
        stub = SinonStub(a, "A_func", my_func)
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

    def test203_constructor_empty_library_function(self):
        def my_func(*args, **kwargs):
            return "my_func"
        self.assertEqual(os.system("cd"), 0)
        stub = SinonStub(os, "system", my_func)
        self.assertEqual(os.system("cd"), "my_func")
        stub.restore()
        self.assertEqual(os.system("cd"), 0)


