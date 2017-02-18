import sys
sys.path.insert(0, '../')

import unittest
import lib.base as sinon
from lib.base import SinonBase

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

    def test000_restore_but_reuse(self):
        base = SinonBase()
        base.restore()
        exception = "weakly-referenced object no longer exists"
        with self.assertRaises(Exception) as context:
            base.called
        self.assertTrue(exception in str(context.exception)) # test weakref errmsg

    def test011_constructor_custom_module(self):
        base = SinonBase(A_object)
        base.restore()

    def test012_constructor_library_module(self):
        base = SinonBase(os)
        base.restore()

    def test013_constructor_module_repeated(self):
        base1 = SinonBase(os)
        with self.assertRaises(Exception) as context:
            base2 = SinonBase(os)
        base1.restore()

    def test014_constructor_module_reassigned(self):
        base = SinonBase(os)
        with self.assertRaises(Exception) as context:
            base = SinonBase(os)
        base.restore()

    def test015_constructor_custom_module_method(self):
        base = SinonBase(A_object, "A_func")
        base.restore()

    def test016_constructor_library_module_method(self):
        base = SinonBase(os, "system")
        base.restore()

    def test017_constructor_module_method_repeated(self):
        base = SinonBase(os, "system")
        with self.assertRaises(Exception) as context:
            base = SinonBase(os, "system")
        base.restore()

    def test018_constructor_empty(self):
        base = SinonBase()
        base.restore()

    def test019_constructor_method(self):
        base = SinonBase(B_func)
        base.restore()

    def test020_constructor_method_repeated(self):
        base = SinonBase(B_func)
        with self.assertRaises(Exception) as context:
            base = SinonBase(B_func)
        base.restore()

    def test021_constructor_instance_method(self):
        A = A_object()
        base = SinonBase(A, "A_func")
        base.restore()

    def test022_constructor_module_variable(self):
        with self.assertRaises(Exception) as context:
            base = SinonBase(os, "path") 

    def test023_constructor_module_repeated(self):
        base = SinonBase(os)
        with self.assertRaises(Exception) as context:
            base = SinonBase(os)
        base.restore()

    def test024_constructor_outside_class(self):
        base = SinonBase(ForTestOnly)
        base.restore()

    def test025_constructor_outside_instance(self):
        fto = ForTestOnly()
        base = SinonBase(fto)
        base.restore()

    def test026_constructor_outside_class_and_instance(self):
        fto = ForTestOnly()
        base1 = SinonBase(ForTestOnly)
        with self.assertRaises(Exception) as context:
            base2 = SinonBase(fto)
        base1.restore()

    def test027_constructor_instance(self):
        A = A_object()
        base = SinonBase(A)
        base.restore()

    def test028_constructor_instance_wrong_method(self):
        A = A_object()
        with self.assertRaises(Exception) as context:
            base = SinonBase(A, "not_exist_function")

    def test029_constructor_invalid_method_type(self):
        A = A_object()
        with self.assertRaises(Exception) as context:
            base = SinonBase(A, 123)
