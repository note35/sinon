import sys
sys.path.insert(0, '../')

import unittest
import lib.SinonBase as sinon
from lib.SinonMock import SinonMock
from lib.SinonSandbox import sinontest

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

class TestSinonMock(unittest.TestCase):
    @sinontest
    def test001_constructor_inside_module(self):
        mock = SinonMock(A_object)
        expectation = mock.expects("A_func") 

    @sinontest
    def test002_constructor_outside_module(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")

    @sinontest
    def test003_constructor_function(self):
        with self.assertRaises(Exception) as context:
            mock = SinonMock(B_func)

    @sinontest
    def test004_constructor_empty(self):
        mock = SinonMock()

    @sinontest
    def test005_constructor_instance(self):
        fto = ForTestOnly()
        mock = SinonMock(fto)
        expectation = mock.expects("func1")

    @sinontest
    def test006_constructor_redeclare_module(self):
        mock = SinonMock(A_object)
        mock = SinonMock(A_object) #nothing will happen


    @sinontest
    def test007_constructor_redeclare_function(self):
        mock = SinonMock(A_object)
        exp1 = mock.expects("A_func")
        with self.assertRaises(Exception) as context:
            exp2 = mock.expects("A_func")

    @sinontest
    def test010_verify_one(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        self.assertTrue(mock.verify()) #no condition

    @sinontest
    def test011_verify_one(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1").once()
        fto = ForTestOnly()
        fto.func1()
        self.assertTrue(mock.verify()) # once condition

    @sinontest
    def test012_verify_one(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1").twice().atLeast(1).atMost(3)
        fto = ForTestOnly()
        fto.func1()
        fto.func1()
        self.assertTrue(mock.verify()) # chain conditions

    @sinontest
    def test013_verify_multi(self):
        mock = SinonMock(ForTestOnly)
        expectation1 = mock.expects("func1").once()
        expectation2 = mock.expects("func2").atMost(1)
        fto = ForTestOnly()
        fto.func1()
        fto.func2()
        self.assertTrue(mock.verify())

    @sinontest
    def test014_verify_empty(self):
        mock = SinonMock(ForTestOnly)
        self.assertTrue(mock.verify()) #no condition

    @sinontest
    def test015_verify_once_with_throws(self):
        mock = SinonMock(ForTestOnly)
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        expectation = mock.expects("func1").once().throws() #spy + stub
        with self.assertRaises(Exception) as context:
            fto.func1()
        self.assertTrue(mock.verify()) 

    @sinontest
    def test016_verify_once_with_returns(self):
        mock = SinonMock(ForTestOnly)
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        expectation = mock.expects("func1").once().returns(None) #spy + stub
        self.assertEqual(fto.func1(), None) 
        self.assertTrue(mock.verify()) 

    @sinontest
    def test030_verify_false(self):
        mock = SinonMock(ForTestOnly)
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        expectation = mock.expects("func1").once().returns(None) #spy + stub
        self.assertFalse(mock.verify()) 

    @sinontest
    def test040_verify_reference_error(self):
        mock = SinonMock(ForTestOnly)
        fto = ForTestOnly()
        self.assertEqual(fto.func1(), "func1")
        expectation = mock.expects("func1").once().returns(None) #spy + stub
        expectation.restore()
        self.assertFalse(mock.verify()) 


class TestSinonMockExpectation(unittest.TestCase):

    """
    Note: all functions in expectation will influence other functions, for testing them, you should
        (1) put assertFalse in your last test because it will never True again
        (2) separate all expectations test without any collision.
    """

    @sinontest
    def test001_atMost(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        self.assertTrue(expectation.verify())
        expectation.atMost(0)
        self.assertTrue(expectation.verify())
        expectation.atMost(1)
        self.assertTrue(expectation.verify())
        expectation.atMost(-1)
        self.assertFalse(expectation.verify())

    @sinontest
    def test002_atMost(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        fto.func1()
        expectation.atMost(1)
        self.assertTrue(expectation.verify())
        expectation.atMost(1).atMost(2).atMost(3)
        self.assertTrue(expectation.verify())
        expectation.atMost(0)
        self.assertFalse(expectation.verify())

    @sinontest
    def test010_atLeast(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        self.assertTrue(expectation.verify())
        expectation.atLeast(0)
        self.assertTrue(expectation.verify())
        expectation.atLeast(-1)
        self.assertTrue(expectation.verify())
        expectation.atLeast(1)
        self.assertFalse(expectation.verify())

    @sinontest
    def test020_never_exactly(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        expectation.never().exactly(0)
        self.assertTrue(expectation.verify())

    @sinontest
    def test021_once_exactly(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        expectation.once().exactly(1)
        self.assertFalse(expectation.verify())
        fto.func1()
        self.assertTrue(expectation.verify())

    @sinontest
    def test022_twice_exactly(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        expectation.twice().exactly(2)
        self.assertFalse(expectation.verify())
        fto.func1()
        fto.func1()
        self.assertTrue(expectation.verify())

    @sinontest
    def test023_thrice_exactly(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        expectation.thrice().exactly(3)
        self.assertFalse(expectation.verify())
        fto.func1()
        fto.func1()
        fto.func1()
        self.assertTrue(expectation.verify())

    @sinontest
    def test030_withArgs_args(self):
        # Todo: source code use a dirty to pass this case, it should be fixed in the future
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        expectation.withArgs("1")
        fto.func1("1")
        self.assertTrue(expectation.verify())

    @sinontest
    def test033_withArgs_kwargs(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        expectation.withExactArgs(opt="1")
        fto.func1(opt="1")
        self.assertTrue(expectation.verify())

    @sinontest
    def test040_withExactArgs_args(self):
        # Todo: source code use a dirty to pass this case, it should be fixed in the future
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        expectation.withExactArgs("1")
        fto.func1("1")
        self.assertTrue(expectation.verify())

    @sinontest
    def test033_withExactArgs_kwargs(self):
        mock = SinonMock(ForTestOnly)
        expectation = mock.expects("func1")
        fto = ForTestOnly()
        expectation.withArgs(opt="1")
        fto.func1(opt="1")
        self.assertTrue(expectation.verify())
