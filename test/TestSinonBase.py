import sys
sys.path.insert(0, '../')

import unittest
import lib.sinon.SinonBase as sinon
from lib.sinon.SinonBase import SinonBase

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
        return "test_global_func"
# global function
def B_func():
    return "test_local_func"
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
        self.assertTrue(exception in str(context.exception))

    def test001_constructor_custom_module(self):
        base = SinonBase(A_object)
        base.restore()

    def test002_constructor_library_module(self):
        base = SinonBase(os)
        base.restore()

    def test003_constructor_module_repeated(self):
        base1 = SinonBase(os)
        exception = "[{}] have already been declared".format(os.__name__)
        with self.assertRaises(Exception) as context:
            base2 = SinonBase(os)
        self.assertTrue(exception in str(context.exception))
        base1.restore()

    def test004_constructor_module_reassigned(self):
        base = SinonBase(os)
        exception = "[{}] have already been declared".format(os.__name__)
        with self.assertRaises(Exception) as context:
            base = SinonBase(os)
        self.assertTrue(exception in str(context.exception))
        base.restore()

    def test005_constructor_custom_module_method(self):
        base = SinonBase(A_object, "A_func")
        base.restore()

    def test006_constructor_library_module_method(self):
        base = SinonBase(os, "system")
        base.restore()

    def test007_constructor_module_method_repeated(self):
        base = SinonBase(os, "system")
        exception = "[{}] have already been declared".format("system")
        with self.assertRaises(Exception) as context:
            base = SinonBase(os, "system")
        self.assertTrue(exception in str(context.exception))
        base.restore()

    def test008_constructor_empty(self):
        base = SinonBase()
        base.restore()

    def test009_constructor_method(self):
        base = SinonBase(B_func)
        base.restore()

    def test010_constructor_method_repeated(self):
        base = SinonBase(B_func)
        exception = "[{}] have already been declared".format(B_func.__name__)
        with self.assertRaises(Exception) as context:
            base = SinonBase(B_func)
        self.assertTrue(exception in str(context.exception))
        base.restore()

    def test011_called_method(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        self.assertTrue(base.called)
        base.restore()


if __name__ == "__main__":
    unittest.main()
