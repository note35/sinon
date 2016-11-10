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
        return "test_global_A_func"
# global function
def B_func():
    return "test_local_B_func"

def C_func(a="a", b="b", c="c"):
    return "test_local_C_func"

def D_func(err=False):
    if err is True:
        raise ValueError("test_local_D_func")
    else:
        return "test_local_D_func"
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

    def test011_calledOnce_method(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        self.assertTrue(base.calledOnce)
        base.restore()

    def test012_calledTwice_method(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(base.calledTwice)
        base.restore()

    def test013_calledThrice_method(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(base.calledThrice)
        base.restore()

    def test014_calledOnce_module_method(self):
        base = SinonBase(os, "system")
        os.system("cd")
        self.assertTrue(base.calledOnce)
        base.restore()

    def test015_calledTwice_module_method(self):
        base = SinonBase(os, "system")
        os.system("cd")
        os.system("cd")
        self.assertTrue(base.calledTwice)
        base.restore()

    def test016_calledThrice_module_method(self):
        base = SinonBase(os, "system")
        os.system("cd")
        os.system("cd")
        os.system("cd")
        self.assertTrue(base.calledThrice)
        base.restore()

    def test017_calledOnce_empty(self):
        base = SinonBase()
        base()
        self.assertTrue(base.calledOnce)
        base.restore()

    def test018_calledTwice_empty(self):
        base = SinonBase()
        base()
        base()
        self.assertTrue(base.calledTwice)
        base.restore()

    def test019_calledThrice_empty(self):
        base = SinonBase()
        base()
        base()
        base()
        self.assertTrue(base.calledThrice)
        base.restore()

    def test020_firstCall_secondCall_thirdCall_lastCall(self):
        base1 = SinonBase(os, "system")
        base2 = SinonBase()
        base3 = SinonBase(B_func)
        base4 = SinonBase()
        os.system("cd")
        base2()
        sinon.g.B_func()
        base4()
        self.assertTrue(base1.firstCall)
        self.assertTrue(base2.secondCall)
        self.assertTrue(base3.thirdCall)
        self.assertTrue(base4.lastCall)
        base1.restore()
        base2.restore()
        base3.restore()
        base4.restore()

    def test021_calledBefore_calledAfter(self):
        base1 = SinonBase(os, "system")
        base2 = SinonBase()
        base3 = SinonBase(B_func)
        os.system("cd")
        base2()
        sinon.g.B_func()
        self.assertTrue(base1.calledBefore(base2))
        self.assertTrue(base1.calledBefore(base3))
        self.assertTrue(base2.calledBefore(base3))
        self.assertTrue(base2.calledAfter(base1))
        self.assertTrue(base3.calledAfter(base1))
        self.assertTrue(base3.calledAfter(base2))
        base1.restore()
        base2.restore()
        base3.restore()

    def test022_calledWithExactly_method_args_only(self):
        base = SinonBase(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(base.calledWithExactly("a", "b", "c"))
        base.restore()

    def test023_calledWithExactly_method_args_only_partial(self):
        base = SinonBase(C_func)
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(base.calledWithExactly("a", "b"))
        base.restore()

    def test050_threw_with_err(self):
        base = SinonBase(D_func)
        sinon.g.D_func(err=True)
        self.assertTrue(base.threw()) 
        base.restore()

    def test051_threw_without_err(self):
        base = SinonBase(D_func)
        sinon.g.D_func(err=False)
        self.assertFalse(base.threw()) 
        base.restore()
