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

    def test011_constructor_custom_module(self):
        base = SinonBase(A_object)
        base.restore()

    def test012_constructor_library_module(self):
        base = SinonBase(os)
        base.restore()

    def test013_constructor_module_repeated(self):
        base1 = SinonBase(os)
        exception = "[{}] have already been declared".format(os.__name__)
        with self.assertRaises(Exception) as context:
            base2 = SinonBase(os)
        self.assertTrue(exception in str(context.exception))
        base1.restore()

    def test014_constructor_module_reassigned(self):
        base = SinonBase(os)
        exception = "[{}] have already been declared".format(os.__name__)
        with self.assertRaises(Exception) as context:
            base = SinonBase(os)
        self.assertTrue(exception in str(context.exception))
        base.restore()

    def test015_constructor_custom_module_method(self):
        base = SinonBase(A_object, "A_func")
        base.restore()

    def test016_constructor_library_module_method(self):
        base = SinonBase(os, "system")
        base.restore()

    def test017_constructor_module_method_repeated(self):
        base = SinonBase(os, "system")
        exception = "[{}] have already been declared".format("system")
        with self.assertRaises(Exception) as context:
            base = SinonBase(os, "system")
        self.assertTrue(exception in str(context.exception))
        base.restore()

    def test018_constructor_empty(self):
        base = SinonBase()
        base.restore()

    def test019_constructor_method(self):
        base = SinonBase(B_func)
        base.restore()

    def test020_constructor_method_repeated(self):
        base = SinonBase(B_func)
        exception = "[{}] have already been declared".format(B_func.__name__)
        with self.assertRaises(Exception) as context:
            base = SinonBase(B_func)
        self.assertTrue(exception in str(context.exception))
        base.restore()

    def test021_constructor_instance(self):
        A = A_object()
        base = SinonBase(A, "A_func")
        base.restore()

    def test040_called_method(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        self.assertTrue(base.called)
        base.restore()

    def test041_calledOnce_method(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        self.assertTrue(base.calledOnce)
        base.restore()

    def test042_calledTwice_method(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(base.calledTwice)
        base.restore()

    def test043_calledThrice_method(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(base.calledThrice)
        base.restore()

    def test044_calledOnce_module_method(self):
        base = SinonBase(os, "system")
        os.system("cd")
        self.assertTrue(base.calledOnce)
        base.restore()

    def test045_calledTwice_module_method(self):
        base = SinonBase(os, "system")
        os.system("cd")
        os.system("cd")
        self.assertTrue(base.calledTwice)
        base.restore()

    def test046_calledThrice_module_method(self):
        base = SinonBase(os, "system")
        os.system("cd")
        os.system("cd")
        os.system("cd")
        self.assertTrue(base.calledThrice)
        base.restore()

    def test047_calledOnce_empty(self):
        base = SinonBase()
        base()
        self.assertTrue(base.calledOnce)
        base.restore()

    def test048_calledTwice_empty(self):
        base = SinonBase()
        base()
        base()
        self.assertTrue(base.calledTwice)
        base.restore()

    def test049_calledThrice_empty(self):
        base = SinonBase()
        base()
        base()
        base()
        self.assertTrue(base.calledThrice)
        base.restore()

    def test050_firstCall_secondCall_thirdCall_lastCall(self):
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

    def test051_calledBefore_calledAfter_normal(self):
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

    def test052_calledBefore_nothing_called(self):
        base1 = SinonBase(os, "system")
        base2 = SinonBase()
        base3 = SinonBase(B_func)
        self.assertFalse(base1.calledBefore(base2))
        self.assertFalse(base2.calledAfter(base1))
        base1.restore()
        base2.restore()

    def test053_calledBefore_calledAfter_recalled_method(self):
        base1 = SinonBase(os, "system")
        base2 = SinonBase()
        os.system("cd")
        base2()
        os.system("cd")
        self.assertTrue(base1.calledBefore(base2))
        self.assertTrue(base1.calledAfter(base2))
        self.assertTrue(base2.calledBefore(base1))
        self.assertTrue(base2.calledAfter(base1))
        base1.restore()
        base2.restore()

    def test054_calledBefore_calledAfter_called_restore_recalled(self):
        base1 = SinonBase(os, "system")
        base2 = SinonBase()
        os.system("cd")
        base1.restore()
        base1 = SinonBase(os, "system")
        base2()
        os.system("cd")
        self.assertTrue(base1.calledAfter(base2))
        self.assertTrue(base2.calledBefore(base1))
        base1.restore()
        base2.restore()

    def test070_calledWith_method_fullmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(base.calledWith(a="a", b="b", c="c"))
        self.assertFalse(base.calledWith(a="wrong", b="b", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(base.calledWith("a", "b", "c"))
        self.assertFalse(base.calledWith("a", "wrong", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(base.calledWith("a", b="b", c="c"))
        self.assertTrue(base.calledWith("a", "b", c="c"))
        self.assertTrue(base.calledWith("a", "b", "c"))
        self.assertFalse(base.calledWith("a", "b", "d"))
        self.assertFalse(base.calledWith("a", "b", c="d"))
        base.restore()

    def test071_calledWith_method_partialmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(base.calledWith(a="wrong"))
        self.assertTrue(base.calledWith(a="a"))
        self.assertTrue(base.calledWith(b="b"))
        self.assertTrue(base.calledWith(c="c"))
        self.assertFalse(base.calledWith(a="wrong", b="b"))
        self.assertTrue(base.calledWith(a="a", b="b"))
        self.assertTrue(base.calledWith(b="b", c="c"))
        self.assertTrue(base.calledWith(a="a", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(base.calledWith("d"))
        self.assertTrue(base.calledWith("a"))
        self.assertTrue(base.calledWith("b"))
        self.assertTrue(base.calledWith("c"))
        self.assertFalse(base.calledWith("wrong", "b"))
        self.assertTrue(base.calledWith("a", "b"))
        self.assertTrue(base.calledWith("b", "c"))
        self.assertTrue(base.calledWith("a", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(base.calledWith("a", b="b"))
        self.assertTrue(base.calledWith("a", c="c"))
        self.assertTrue(base.calledWith(b="b", c="c"))
        self.assertTrue(base.calledWith("a"))
        self.assertTrue(base.calledWith(c="c"))
        self.assertFalse(base.calledWith("wrong", b="b"))
        self.assertFalse(base.calledWith("a", b="wrong"))
        self.assertFalse(base.calledWith("a", c="wrong"))
        base.restore()

    def test072_alwaysCalledWith_method_fullmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(base.alwaysCalledWith(a="a", b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(base.alwaysCalledWith(a="a", b="b", c="c"))
        base.restore()
        base = SinonBase(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(base.alwaysCalledWith("a", "b", "c"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(base.alwaysCalledWith("a", "b", "c"))
        base.restore()
        base = SinonBase(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(base.alwaysCalledWith("a", b="b", c="c"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(base.alwaysCalledWith("a", b="b", c="c"))
        base.restore()

    def test073_alwaysCalledWith_method_partialmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="xxxx", b="b", c="c")
        self.assertTrue(base.alwaysCalledWith(b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(base.alwaysCalledWith(b="b", c="c"))
        base.restore()
        base = SinonBase(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "xxxx")
        self.assertTrue(base.alwaysCalledWith("a", "b"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(base.alwaysCalledWith("a", "b"))
        base.restore()
        base = SinonBase(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b")
        self.assertTrue(base.alwaysCalledWith("a", b="b"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(base.alwaysCalledWith("a", b="b"))
        base.restore()

    def test074_calledWithExactly_method_fullmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(base.calledWithExactly(a="a", b="b", c="c"))
        self.assertFalse(base.calledWithExactly(a="d", b="e", c="f"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(base.calledWithExactly("a", "b", "c"))
        self.assertFalse(base.calledWithExactly("d", "e", "f"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(base.calledWithExactly("a", b="b", c="c"))
        self.assertFalse(base.calledWithExactly("wrong", b="b", c="c"))
        base.restore()

    def test075_calledWithExactly_method_partialmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(base.calledWithExactly(a="a", b="b"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(base.calledWithExactly("a", "b"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(base.calledWithExactly("a", b="b"))
        base.restore()

    def test076_alwaysCalledWithExactly_method_fullmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(base.alwaysCalledWithExactly(a="a", b="b", c="c"))
        sinon.g.C_func(a="d", b="e", c="f")
        self.assertFalse(base.alwaysCalledWithExactly(a="a", b="b", c="c"))
        base.restore()
        base = SinonBase(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(base.alwaysCalledWithExactly("a", "b", "c"))
        sinon.g.C_func("d", "e", "f")
        self.assertFalse(base.alwaysCalledWithExactly("a", "b", "c"))
        base.restore()
        base = SinonBase(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(base.alwaysCalledWithExactly("a", b="b", c="c"))
        sinon.g.C_func("b", b="b", c="c")
        self.assertFalse(base.alwaysCalledWithExactly("a", b="b", c="c"))
        base.restore()

    def test077_alwaysCalledWithExactly_method_partialmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(base.alwaysCalledWithExactly(a="a", b="b", c="c"))
        sinon.g.C_func(a="xxxx", b="b", c="c")
        self.assertFalse(base.alwaysCalledWithExactly(b="b", c="c"))
        base.restore()
        base = SinonBase(C_func)
        #pure args
        sinon.g.C_func("a", "b", "c")
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(base.alwaysCalledWithExactly("a", "b", "c"))
        sinon.g.C_func("a", "b", "xxxx")
        self.assertFalse(base.alwaysCalledWithExactly("a", "b"))
        base.restore()
        base = SinonBase(C_func)
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        sinon.g.C_func("a", b="b", c="c")
        self.assertTrue(base.alwaysCalledWithExactly("a", b="b", c="c"))
        sinon.g.C_func("a", b="b", c="xxx")
        self.assertFalse(base.alwaysCalledWithExactly("a", b="b"))
        base.restore()

    def test078_neverCalledWith_method_fullmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertFalse(base.neverCalledWith(a="a", b="b", c="c"))
        self.assertTrue(base.neverCalledWith(a="wrong", b="b", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertFalse(base.neverCalledWith("a", "b", "c"))
        self.assertTrue(base.neverCalledWith("a", "wrong", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(base.neverCalledWith("a", b="b", c="c"))
        self.assertFalse(base.neverCalledWith("a", "b", c="c"))
        self.assertFalse(base.neverCalledWith("a", "b", "c"))
        self.assertTrue(base.neverCalledWith("a", "b", "d"))
        self.assertTrue(base.neverCalledWith("a", "b", c="d"))
        base.restore()

    def test079_neverCalledWith_method_partialmatch(self):
        base = SinonBase(C_func)
        #pure kwargs
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertTrue(base.neverCalledWith(a="wrong"))
        self.assertFalse(base.neverCalledWith(a="a"))
        self.assertFalse(base.neverCalledWith(b="b"))
        self.assertFalse(base.neverCalledWith(c="c"))
        self.assertTrue(base.neverCalledWith(a="wrong", b="b"))
        self.assertFalse(base.neverCalledWith(a="a", b="b"))
        self.assertFalse(base.neverCalledWith(b="b", c="c"))
        self.assertFalse(base.neverCalledWith(a="a", c="c"))
        #pure args
        sinon.g.C_func("a", "b", "c")
        self.assertTrue(base.neverCalledWith("d"))
        self.assertFalse(base.neverCalledWith("a"))
        self.assertFalse(base.neverCalledWith("b"))
        self.assertFalse(base.neverCalledWith("c"))
        self.assertTrue(base.neverCalledWith("wrong", "b"))
        self.assertFalse(base.neverCalledWith("a", "b"))
        self.assertFalse(base.neverCalledWith("b", "c"))
        self.assertFalse(base.neverCalledWith("a", "c"))
        #combine kwargs and args
        sinon.g.C_func("a", b="b", c="c")
        self.assertFalse(base.neverCalledWith("a", b="b"))
        self.assertFalse(base.neverCalledWith("a", c="c"))
        self.assertFalse(base.neverCalledWith(b="b", c="c"))
        self.assertFalse(base.neverCalledWith("a"))
        self.assertFalse(base.neverCalledWith(c="c"))
        self.assertTrue(base.neverCalledWith("wrong", b="b"))
        self.assertTrue(base.neverCalledWith("a", b="wrong"))
        self.assertTrue(base.neverCalledWith("a", c="wrong"))
        base.restore()

    def test090_threw_without_err(self):
        base = SinonBase(D_func)
        sinon.g.D_func(err=False)
        self.assertFalse(base.threw()) 
        base.restore()

    def test091_threw_with_err(self):
        class MyException(Exception):
            pass
        base = SinonBase(D_func)
        sinon.g.D_func(err=MyException)
        self.assertTrue(base.threw()) 
        self.assertTrue(base.threw(MyException))
        self.assertFalse(base.threw(ValueError))
        sinon.g.D_func(err=ValueError)
        self.assertTrue(base.threw(ValueError))
        base.restore()

    def test092_alwaysThrew_without_err(self):
        base = SinonBase(D_func)
        sinon.g.D_func(err=False)
        sinon.g.D_func(err=False)
        self.assertFalse(base.alwaysThrew()) 
        base.restore()

    def test093_alwaysThrew_with_same_err(self):
        class MyException(Exception):
            pass
        base = SinonBase(D_func)
        sinon.g.D_func(err=MyException)
        sinon.g.D_func(err=MyException)
        self.assertTrue(base.alwaysThrew()) 
        self.assertTrue(base.alwaysThrew(MyException))
        sinon.g.D_func(err=ValueError)
        self.assertFalse(base.alwaysThrew(MyException))
        base.restore()

    def test100_returned(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        self.assertTrue(base.returned("test_local_B_func"))
        sinon.g.B_func(2)
        self.assertTrue(base.returned("test_local_B_func2"))
        base.restore()

    def test101_returned_exception(self):
        # exception will return a empty function with no return
        base = SinonBase(D_func)
        sinon.g.D_func(err=ValueError)
        self.assertFalse(base.returned("test_local_D_func"))
        sinon.g.D_func()
        self.assertTrue(base.returned("test_local_D_func"))
        base.restore()

    def test102_alwaysReturned(self):
        base = SinonBase(B_func)
        sinon.g.B_func()
        sinon.g.B_func()
        self.assertTrue(base.alwaysReturned("test_local_B_func"))
        sinon.g.B_func(123)
        self.assertFalse(base.alwaysReturned("test_local_B_func"))
        base.restore() 

    def test110_getCall(self):
        base1 = SinonBase(B_func)
        base2 = SinonBase(C_func)
        sinon.g.B_func()
        call = SinonBase.getCall(1)
        self.assertFalse(base2.called)  #C_func is never called
        self.assertTrue(call.called)    #B_func is called
        base1.restore() 
        base2.restore()

    def test111_getCall_wrongIndex(self):
        exception = "The call queue only contains 1 calls"
        with self.assertRaises(Exception) as context:
            SinonBase.getCall(100)
        self.assertTrue(exception in str(context.exception))

    def test120_kwargs(self):
        base = SinonBase(C_func)
        self.assertEqual(base.kwargs, [])
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertEqual(base.kwargs, [{"a":"a", "b":"b", "c":"c"}])
        sinon.g.C_func(a="a", b="b", c="c")
        self.assertEqual(base.kwargs, [{"a":"a", "b":"b", "c":"c"}, {"a":"a", "b":"b", "c":"c"}])
        sinon.g.C_func("a", b="b", c="c")
        self.assertEqual(base.kwargs, [{"a":"a", "b":"b", "c":"c"}, {"a":"a", "b":"b", "c":"c"}, {"b": "b", "c": "c"}])
        base.restore()

    def test121_args(self):
        base = SinonBase(C_func)
        self.assertEqual(base.args, [])
        sinon.g.C_func("a", "b", "c")
        self.assertEqual(base.args, [("a", "b", "c")])
        sinon.g.C_func("a", "b", "c")
        self.assertEqual(base.args, [("a", "b", "c"), ("a", "b", "c")])
        sinon.g.C_func("a", b="b", c="c")
        self.assertEqual(base.args, [("a", "b", "c"), ("a", "b", "c"), ("a",)])
        base.restore()

    def test122_exceptions(self):
        base = SinonBase(D_func)
        self.assertEqual(base.exceptions, [])
        sinon.g.D_func(ValueError)
        self.assertEqual(base.exceptions, [ValueError])
        sinon.g.D_func(TypeError)
        self.assertEqual(base.exceptions, [ValueError, TypeError])
        base.restore()

    def test123_returnValues(self):
        base = SinonBase(B_func)
        self.assertEqual(base.exceptions, [])
        sinon.g.B_func()
        self.assertEqual(base.returnValues, ["test_local_B_func"])
        sinon.g.B_func(2)
        self.assertEqual(base.returnValues, ["test_local_B_func", "test_local_B_func2"])
        base.restore()

    def test130_reset(self):
        base = SinonBase(B_func)
        sinon.g.B_func(2)
        self.assertTrue(base.called)
        self.assertTrue(base.args)
        base.reset()
        self.assertFalse(base.called)
        self.assertFalse(base.args)
        base.restore()
